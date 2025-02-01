-- MySQL dump 10.13  Distrib 9.1.0, for macos14 (arm64)
--
-- Host: localhost    Database: Bibliotheque
-- ------------------------------------------------------
-- Server version	9.1.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `EMPRUNT`
--

DROP TABLE IF EXISTS `EMPRUNT`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `EMPRUNT` (
  `id_emprunt` int NOT NULL AUTO_INCREMENT,
  `id_usager` int DEFAULT NULL,
  `id_livre` int DEFAULT NULL,
  `date_emprunt` date NOT NULL,
  `date_retour` datetime DEFAULT NULL,
  PRIMARY KEY (`id_emprunt`),
  KEY `id_usager` (`id_usager`),
  KEY `id_livre` (`id_livre`),
  CONSTRAINT `emprunt_ibfk_1` FOREIGN KEY (`id_usager`) REFERENCES `USAGER` (`id_usager`),
  CONSTRAINT `emprunt_ibfk_2` FOREIGN KEY (`id_livre`) REFERENCES `LIVRE` (`id_livre`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `EMPRUNT`
--

LOCK TABLES `EMPRUNT` WRITE;
/*!40000 ALTER TABLE `EMPRUNT` DISABLE KEYS */;
INSERT INTO `EMPRUNT` VALUES (1,1,1,'2025-02-01','2025-02-01 20:16:00'),(7,1,1,'2025-02-02','2025-02-02 01:16:41'),(8,2,3,'2025-02-02','2025-02-02 00:50:47'),(9,3,7,'2025-02-02',NULL);
/*!40000 ALTER TABLE `EMPRUNT` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `LIVRE`
--

DROP TABLE IF EXISTS `LIVRE`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `LIVRE` (
  `id_livre` int NOT NULL AUTO_INCREMENT,
  `titre` varchar(255) NOT NULL,
  `auteur` varchar(100) NOT NULL,
  `categorie` varchar(50) DEFAULT NULL,
  `disponibilite` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id_livre`),
  UNIQUE KEY `unique_livre` (`titre`,`auteur`,`categorie`)
) ENGINE=InnoDB AUTO_INCREMENT=72 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `LIVRE`
--

LOCK TABLES `LIVRE` WRITE;
/*!40000 ALTER TABLE `LIVRE` DISABLE KEYS */;
INSERT INTO `LIVRE` VALUES (1,'Le Petit Prince','Antoine de Saint-Exupéry','Roman',1),(2,'1984','George Orwell','Science Fiction',1),(3,'Crime et Châtiment','Fiodor Dostoïevski','Classique',1),(7,'Harry Potter à l\'école des sorciers','J.K. Rowling','Fantasy',0),(8,'Le Seigneur des Anneaux','J.R.R. Tolkien','Fantasy',1),(9,'Game of Thrones','George R.R. Martin','Fantasy',1),(10,'Les Misérables','Victor Hugo','Classique',1),(11,'Germinal','Émile Zola','Classique',1),(12,'L\'Étranger','Albert Camus','Philosophie',1),(13,'La Peste','Albert Camus','Philosophie',1),(16,'Le Meilleur des mondes','Aldous Huxley','Science Fiction',1),(17,'Fondation','Isaac Asimov','Science Fiction',1),(18,'Dune','Frank Herbert','Science Fiction',1),(19,'Sherlock Holmes: Une étude en rouge','Arthur Conan Doyle','Policier',1),(20,'Le Crime de l\'Orient-Express','Agatha Christie','Policier',1),(21,'Da Vinci Code','Dan Brown','Thriller',1),(22,'Les Fourmis','Bernard Werber','Science Fiction',1),(23,'L\'Alchimiste','Paulo Coelho','Développement personnel',1),(24,'Père riche, père pauvre','Robert Kiyosaki','Économie',1),(25,'Sapiens: Une brève histoire de l\'humanité','Yuval Noah Harari','Histoire',1),(26,'L\'art de la guerre','Sun Tzu','Stratégie',1);
/*!40000 ALTER TABLE `LIVRE` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `RESERVATION`
--

DROP TABLE IF EXISTS `RESERVATION`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `RESERVATION` (
  `id_reservation` int NOT NULL AUTO_INCREMENT,
  `id_usager` int DEFAULT NULL,
  `id_livre` int DEFAULT NULL,
  `date_reservation` date NOT NULL,
  PRIMARY KEY (`id_reservation`),
  KEY `id_usager` (`id_usager`),
  KEY `id_livre` (`id_livre`),
  CONSTRAINT `reservation_ibfk_1` FOREIGN KEY (`id_usager`) REFERENCES `USAGER` (`id_usager`),
  CONSTRAINT `reservation_ibfk_2` FOREIGN KEY (`id_livre`) REFERENCES `LIVRE` (`id_livre`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `RESERVATION`
--

LOCK TABLES `RESERVATION` WRITE;
/*!40000 ALTER TABLE `RESERVATION` DISABLE KEYS */;
INSERT INTO `RESERVATION` VALUES (1,2,1,'2025-02-01');
/*!40000 ALTER TABLE `RESERVATION` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `USAGER`
--

DROP TABLE IF EXISTS `USAGER`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `USAGER` (
  `id_usager` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(50) NOT NULL,
  `prenom` varchar(50) NOT NULL,
  `adresse` varchar(255) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `telephone` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`id_usager`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `telephone` (`telephone`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `USAGER`
--

LOCK TABLES `USAGER` WRITE;
/*!40000 ALTER TABLE `USAGER` DISABLE KEYS */;
INSERT INTO `USAGER` VALUES (1,'Kim','Minho','Seoul, Korea','minho.kim@email.com','010-1234-5678'),(2,'Park','Jisoo','Busan, Korea','jisoo.park@email.com','010-9876-5432'),(3,'Yeo','Chaeryeong',NULL,'ycr0102@gmail.com',NULL),(5,'Yeo','sherry',NULL,'y_cr0102@naver.com',NULL),(6,'Smith','Wurtz','France','s.wurtz@google.com','0733445566'),(7,'Tissue','Will','USA','willtissue@gmail.com','10333322');
/*!40000 ALTER TABLE `USAGER` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-02-02  2:05:14
