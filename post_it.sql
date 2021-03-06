-- MySQL dump 10.13  Distrib 5.5.62, for Win64 (AMD64)
--
-- Host: 34.136.217.246    Database: post_it
-- ------------------------------------------------------
-- Server version	5.5.5-10.4.18-MariaDB-1:10.4.18+maria~stretch

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `comment`
--

DROP TABLE IF EXISTS `comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `comment` (
  `content` varchar(150) NOT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `user_id` int(10) unsigned NOT NULL,
  `tweet_id` int(10) unsigned NOT NULL,
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  KEY `comment_FK` (`user_id`),
  KEY `comment_FK_1` (`tweet_id`),
  CONSTRAINT `comment_FK` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `comment_FK_1` FOREIGN KEY (`tweet_id`) REFERENCES `tweet` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=59 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comment`
--

LOCK TABLES `comment` WRITE;
/*!40000 ALTER TABLE `comment` DISABLE KEYS */;
INSERT INTO `comment` VALUES ('Hi Emily, it\'s nice to meet you!','2021-07-07 19:53:55',44,49,50),('Welcome to Post It, Emily!','2021-07-07 19:54:25',45,49,51),('Good luck on your finals, William!','2021-07-09 17:50:42',45,53,54),('I would love to connect with you, Rebecca! Here\'s a link to my LinkedIn: www.linkedin.com/in/monicatamang/','2021-07-09 17:58:23',43,54,55),('Feel free to connect with me on LinkedIn: www.linkedin.com/in/williammurdoch. Look forward to staying connected','2021-07-09 18:01:31',44,54,56),('Congratulations, Rebecca! So happy for you!','2021-07-09 18:13:18',43,56,57),('Congratulations, Rebecca','2021-07-09 18:14:33',44,56,58);
/*!40000 ALTER TABLE `comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comment_like`
--

DROP TABLE IF EXISTS `comment_like`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `comment_like` (
  `user_id` int(10) unsigned NOT NULL,
  `comment_id` int(10) unsigned NOT NULL,
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `created_at` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `comment_likes_un` (`user_id`,`comment_id`),
  KEY `comment_likes_FK` (`user_id`),
  KEY `comment_likes_FK_1` (`comment_id`),
  CONSTRAINT `comment_likes_FK` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `comment_likes_FK_1` FOREIGN KEY (`comment_id`) REFERENCES `comment` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comment_like`
--

LOCK TABLES `comment_like` WRITE;
/*!40000 ALTER TABLE `comment_like` DISABLE KEYS */;
INSERT INTO `comment_like` VALUES (43,50,20,'2021-07-07 19:55:57'),(43,51,21,'2021-07-07 19:56:01'),(44,54,24,'2021-07-09 18:02:19'),(45,58,25,'2021-07-09 18:15:09'),(45,57,26,'2021-07-09 18:15:11');
/*!40000 ALTER TABLE `comment_like` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `follow`
--

DROP TABLE IF EXISTS `follow`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `follow` (
  `follower_id` int(10) unsigned NOT NULL,
  `follow_id` int(10) unsigned NOT NULL,
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `created_at` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `follow_un` (`follower_id`,`follow_id`),
  KEY `follow_FK_1` (`follow_id`),
  CONSTRAINT `follow_FK` FOREIGN KEY (`follower_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `follow_FK_1` FOREIGN KEY (`follow_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `follow_check` CHECK (`follower_id` <> `follow_id`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `follow`
--

LOCK TABLES `follow` WRITE;
/*!40000 ALTER TABLE `follow` DISABLE KEYS */;
INSERT INTO `follow` VALUES (43,44,26,'2021-07-07 19:56:34'),(44,43,28,'2021-07-07 19:57:00'),(44,45,29,'2021-07-07 19:57:04'),(45,43,30,'2021-07-07 19:57:16'),(45,44,31,'2021-07-07 19:57:19'),(43,45,35,'2021-07-09 17:22:37');
/*!40000 ALTER TABLE `follow` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tweet`
--

DROP TABLE IF EXISTS `tweet`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tweet` (
  `content` varchar(200) NOT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `user_id` int(10) unsigned NOT NULL,
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  KEY `tweet_FK` (`user_id`),
  CONSTRAINT `tweet_FK` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=57 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tweet`
--

LOCK TABLES `tweet` WRITE;
/*!40000 ALTER TABLE `tweet` DISABLE KEYS */;
INSERT INTO `tweet` VALUES ('Hi everyone, I\'m Emily! It\'s my first time being on this platform and I\'m super excited to expand my network and make new connections!','2021-07-07 19:51:20',43,49),('Last day of finals!','2021-07-09 17:47:29',44,53),('Hi everyone! I\'m currently in my final year of Chemistry and looking to expand my network on LinkedIn. Does anyone want to connect on LinkedIn?','2021-07-09 17:54:17',45,54),('First day of my nursing practicum! Nervous but excited!!!','2021-07-09 18:05:31',43,55),('Got accepted into the Masters of Science in Chemistry program!!!!!!!!!!!!!!!','2021-07-09 18:12:07',45,56);
/*!40000 ALTER TABLE `tweet` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tweet_like`
--

DROP TABLE IF EXISTS `tweet_like`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tweet_like` (
  `user_id` int(10) unsigned NOT NULL,
  `tweet_id` int(10) unsigned NOT NULL,
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `created_at` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `tweet_likes_un` (`user_id`,`tweet_id`),
  KEY `tweet_likes_FK` (`user_id`),
  KEY `tweet_likes_FK_1` (`tweet_id`),
  CONSTRAINT `tweet_likes_FK` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `tweet_likes_FK_1` FOREIGN KEY (`tweet_id`) REFERENCES `tweet` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tweet_like`
--

LOCK TABLES `tweet_like` WRITE;
/*!40000 ALTER TABLE `tweet_like` DISABLE KEYS */;
INSERT INTO `tweet_like` VALUES (44,49,18,'2021-07-07 19:55:16'),(45,49,19,'2021-07-07 19:55:30'),(45,53,21,'2021-07-09 17:50:27'),(43,54,22,'2021-07-09 17:57:15'),(44,54,23,'2021-07-09 18:00:14'),(43,53,24,'2021-07-09 18:06:03'),(45,55,25,'2021-07-09 18:07:45'),(43,56,26,'2021-07-09 18:12:56'),(44,56,27,'2021-07-09 18:14:17');
/*!40000 ALTER TABLE `tweet_like` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_session`
--

DROP TABLE IF EXISTS `user_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_session` (
  `user_id` int(10) unsigned NOT NULL,
  `token` varchar(100) NOT NULL,
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_session_UN` (`token`),
  KEY `user_session_FK` (`user_id`),
  CONSTRAINT `user_session_FK` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=106 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_session`
--

LOCK TABLES `user_session` WRITE;
/*!40000 ALTER TABLE `user_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `username` varchar(30) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(150) NOT NULL,
  `bio` varchar(160) DEFAULT '',
  `birthdate` date NOT NULL,
  `image_url` text DEFAULT '',
  `created_at` datetime DEFAULT current_timestamp(),
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `salt` varchar(10) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `users_UN_1` (`username`),
  UNIQUE KEY `users_UN_2` (`email`),
  CONSTRAINT `users_check` CHECK (char_length(`password`) > 12)
) ENGINE=InnoDB AUTO_INCREMENT=48 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES ('emilygrace','emilygrace@ucalgary.ca','cc0849b676b7681ec68444558824a0003bb8398c84525165ebde862fc8c4c4b280bdaa19d9037dcebc498a16a7aee8b7f04e606dae7732385ffd45615fbac763','Second Year Nursing Student at the University of Calgary','1997-05-21','https://www.robertmcgee.ca/wp-content/uploads/2020/02/LinkedIn-headshot-for-Shanee-wearing-black-jacket-019A0845.jpg','2021-07-07 19:40:05',43,'UMoR0keqZB'),('williammurdoch','williammurdoch@ucambridge.uk','fe04a3db17040276885f943992f82ecd18f1ed0e9b7ab70c2ac6ce5180742671d8ea678a0a21f3249494976fc4fc2c9e8eb0f6818ab747c3c4ef77a17fbf841e','Third Year Kinesiology Student at the University of Cambridge','1996-03-09',NULL,'2021-07-07 19:41:47',44,'UJMZpPKyFB'),('rebeccajames','rebeccajames@utoronto.ca','3fa499cc00a504c64801e7719ac7062ce9776153341f27c1a52859361f67b345490a1f961cefb8280d803dd573eea080bcda6ec6e7a0669e0d1e5df81df3adf9','Fourth Year Chemistry Student at the University of Toronto','2000-12-27','https://d5t4h5a9.rocketcdn.me/wp-content/uploads/2021/02/Website-Photo-11-1.jpg','2021-07-07 19:45:00',45,'adSlOFJ0Vw');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'post_it'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-07-09 12:37:08
