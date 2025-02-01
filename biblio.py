from flask import Flask, request, jsonify, render_template
import mysql.connector
import os

app = Flask(__name__)

@app.route('/')
def home():
    # 홈 페이지를 보여주기 위해 기본 템플릿을 렌더링합니다.
    return render_template('recherche.html')

@app.route('/recherche', methods=['POST'])
def recherche_livres():
    data = request.get_json()
    query = data.get('query')

    if not query or not isinstance(query, str):
        return jsonify([])  # 빈 리스트 반환 (결과 없음)

    try:
        # 데이터베이스 연결 생성
        db = mysql.connector.connect(
            host="localhost",
            user=os.environ.get("DB_USER", "root"),
            password=os.environ.get("DB_PASSWORD", "rootroot"),
            database=os.environ.get("DB_NAME", "Bibliotheque")
        )
        cursor = db.cursor(dictionary=True)

        # SQL 쿼리 실행
        sql = "SELECT id_livre, titre, auteur, categorie, disponibilite FROM LIVRE WHERE LOWER(titre) LIKE %s"
        cursor.execute(sql, (f"%{query}%",))
        results = cursor.fetchall()

    except mysql.connector.Error as err:
        return jsonify({"error": f"Erreur de base de données : {str(err)}"}), 500

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

    # 검색 결과 반환
    return jsonify(results)

@app.route('/detail')
def detail():
    # URL에서 'id' 매개변수 가져오기
    livre_id = request.args.get('id')

    # ID가 없으면 404 반환
    if not livre_id:
        return "<h1>Livre non trouvé</h1>", 404

    return render_template('detail.html')

@app.route('/api/livre/<int:livre_id>', methods=['GET'])
def get_livre_details(livre_id):
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="rootroot",
            database="Bibliotheque"
        )
        cursor = db.cursor(dictionary=True)

        # 도서 정보 가져오기
        cursor.execute("""
            SELECT 
                LIVRE.id_livre, 
                LIVRE.titre, 
                LIVRE.auteur, 
                LIVRE.categorie, 
                LIVRE.disponibilite,
                (SELECT COUNT(*) FROM EMPRUNT WHERE id_livre = LIVRE.id_livre AND date_retour IS NULL) AS en_emprunt,
                (SELECT CONCAT(USAGER.nom, ' ', USAGER.prenom) FROM EMPRUNT 
                    INNER JOIN USAGER ON EMPRUNT.id_usager = USAGER.id_usager
                    WHERE EMPRUNT.id_livre = LIVRE.id_livre AND EMPRUNT.date_retour IS NULL LIMIT 1) AS dernier_emprunteur,
                (SELECT MAX(EMPRUNT.date_emprunt) FROM EMPRUNT 
                    WHERE EMPRUNT.id_livre = LIVRE.id_livre) AS derniere_date_emprunt,
                (SELECT MAX(EMPRUNT.date_retour) FROM EMPRUNT 
                    WHERE EMPRUNT.id_livre = LIVRE.id_livre) AS date_retour
            FROM LIVRE
            WHERE LIVRE.id_livre = %s
        """, (livre_id,))
        livre = cursor.fetchone()

        if not livre:
            return jsonify({"error": "Livre non trouvé"}), 404

        # `en_emprunt` 값을 Boolean으로 변환
        livre["en_emprunt"] = True if livre["en_emprunt"] > 0 else False

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        cursor.close()
        db.close()

    return jsonify(livre)


@app.route('/emprunter', methods=['POST'])
def emprunter_livre():
    data = request.get_json()
    id_usager = data.get("id_usager")
    id_livre = data.get("id_livre")

    if not id_usager or not id_livre:
        return jsonify({"error": "ID utilisateur et ID livre requis"}), 400

    try:
        db = mysql.connector.connect(host="localhost", user="root", password="rootroot", database="Bibliotheque")
        cursor = db.cursor()

        # 사용자의 현재 대출 권수 확인
        cursor.execute("SELECT COUNT(*) FROM EMPRUNT WHERE id_usager = %s AND date_retour IS NULL", (id_usager,))
        nb_emprunts = cursor.fetchone()[0]

        if nb_emprunts >= 5:
            return jsonify({"error": "Vous avez déjà emprunté 5 livres"}), 400

        # 책이 대출 가능한 상태인지 확인
        cursor.execute("SELECT disponibilite FROM LIVRE WHERE id_livre = %s", (id_livre,))
        livre_status = cursor.fetchone()

        if not livre_status or livre_status[0] == 0:
            return jsonify({"error": "Ce livre est déjà emprunté"}), 400

        # 대출 기록 추가
        cursor.execute("INSERT INTO EMPRUNT (id_usager, id_livre, date_emprunt) VALUES (%s, %s, NOW())", (id_usager, id_livre))

        # 책 상태 변경 (대출 불가능)
        cursor.execute("UPDATE LIVRE SET disponibilite = FALSE WHERE id_livre = %s", (id_livre,))
        db.commit()

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        cursor.close()
        db.close()

    return jsonify({"message": "Livre emprunté avec succès!"}), 200



@app.route('/reserver', methods=['POST'])
def reserver_livre():
    try:
        data = request.get_json()
        id_usager = data.get("id_usager")
        id_livre = data.get("id_livre")

        if not id_usager or not id_livre:
            return jsonify({"error": "ID utilisateur et ID livre requis"}), 400

        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="rootroot",
            database="Bibliotheque"
        )
        cursor = db.cursor()

        # 대여 중인 도서만 예약 가능
        cursor.execute("SELECT disponibilite FROM LIVRE WHERE id_livre = %s", (id_livre,))
        livre = cursor.fetchone()
        if not livre or livre[0]:  # disponible = True
            return jsonify({"error": "Ce livre est disponible, vous ne pouvez pas le réserver."}), 400

        # 예약 추가
        cursor.execute("""
            INSERT INTO RESERVATION (id_usager, id_livre, date_reservation) 
            VALUES (%s, %s, NOW())
        """, (id_usager, id_livre))
        db.commit()

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        cursor.close()
        db.close()

    return jsonify({"message": "Réservation effectuée avec succès!"}), 201




@app.route('/retourner', methods=['POST'])
def retourner_livre():
    data = request.get_json()
    id_usager = data.get("id_usager")
    id_livre = data.get("id_livre")  # 사용자가 반납할 책의 ID

    if not id_usager or not id_livre:
        return jsonify({"error": "ID utilisateur et ID livre requis"}), 400

    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="rootroot",
            database="Bibliotheque"
        )
        cursor = db.cursor()

        # 사용자가 대출 중인 해당 책의 대출 정보 가져오기
        cursor.execute("""
            SELECT id_emprunt FROM EMPRUNT 
            WHERE id_usager = %s AND id_livre = %s AND date_retour IS NULL
        """, (id_usager, id_livre))
        emprunt = cursor.fetchone()

        if not emprunt:
            return jsonify({"error": "Aucun emprunt actif trouvé pour cet utilisateur et ce livre"}), 400

        id_emprunt = emprunt[0]

        # 반납 처리
        cursor.execute("UPDATE EMPRUNT SET date_retour = NOW() WHERE id_emprunt = %s", (id_emprunt,))
        cursor.execute("UPDATE LIVRE SET disponibilite = TRUE WHERE id_livre = %s", (id_livre,))
        db.commit()

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        cursor.close()
        db.close()

    return jsonify({"message": "Livre retourné avec succès!"}), 200



@app.route('/statistiques', methods=['GET'])
def statistiques():
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="rootroot",
            database="Bibliotheque"
        )
        cursor = db.cursor(dictionary=True)

        cursor.execute("SELECT COUNT(*) AS total_emprunts FROM EMPRUNT")
        total_emprunts = cursor.fetchone()['total_emprunts']

        cursor.execute("SELECT COUNT(*) AS total_reservations FROM RESERVATION")
        total_reservations = cursor.fetchone()['total_reservations']

        cursor.execute("""
            SELECT 
                (SELECT COUNT(*) FROM EMPRUNT) / NULLIF((SELECT COUNT(*) FROM LIVRE), 0) AS taux_rotation
        """)
        taux_rotation = cursor.fetchone()['taux_rotation']

        if taux_rotation is None:
            taux_rotation = 0

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        cursor.close()
        db.close()

    return jsonify({
        "total_emprunts": total_emprunts,
        "total_reservations": total_reservations,
        "taux_rotation": float(taux_rotation)  
    })



@app.route('/usagers', methods=['POST'])
def ajouter_usager():
    try:
        data = request.get_json()
        nom = data.get("nom")
        prenom = data.get("prenom")
        email = data.get("email")
        adresse = data.get("adresse") 
        telephone = data.get("telephone") 

        if not nom or not prenom or not email:
            return jsonify({"error": "Nom, prénom et email sont obligatoires."}), 400

        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="rootroot",
            database="Bibliotheque"
        )
        cursor = db.cursor()

        cursor.execute("""
            INSERT INTO USAGER (nom, prenom, email, adresse, telephone) 
            VALUES (%s, %s, %s, %s, %s)
        """, (nom, prenom, email, adresse, telephone))
        
        db.commit()

    except mysql.connector.IntegrityError:
        return jsonify({"error": "Cet email est déjà utilisé. Veuillez en choisir un autre."}), 400

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        cursor.close()
        db.close()

    return jsonify({"message": "Utilisateur ajouté avec succès!"}), 201



# 📌 Flask 실행
if __name__ == '__main__':
    app.run(debug=True)
