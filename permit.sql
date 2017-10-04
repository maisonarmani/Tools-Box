-- MySQL dump 10.16  Distrib 10.1.23-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: 1bd3e0294da19198
-- ------------------------------------------------------
-- Server version	10.1.23-MariaDB

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
-- Table structure for table `tabContractor Permit to Work`
--

DROP TABLE IF EXISTS `tabContractor Permit to Work`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabContractor Permit to Work` (
  `name` varchar(140) COLLATE utf8mb4_unicode_ci NOT NULL,
  `creation` datetime(6) DEFAULT NULL,
  `modified` datetime(6) DEFAULT NULL,
  `modified_by` varchar(140) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `owner` varchar(140) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `docstatus` int(1) NOT NULL DEFAULT '0',
  `parent` varchar(140) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `parentfield` varchar(140) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `parenttype` varchar(140) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `idx` int(8) NOT NULL DEFAULT '0',
  `coverall` int(1) NOT NULL DEFAULT '0',
  `supervisor` varchar(140) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `excavation_or_trenching` int(1) NOT NULL DEFAULT '0',
  `supervisor_fullname` varchar(140) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `erecting_scaffolding` int(1) NOT NULL DEFAULT '0',
  `screens` int(1) NOT NULL DEFAULT '0',
  `the_hazards_involved_in_this_work_include` text COLLATE utf8mb4_unicode_ci,
  `_liked_by` text COLLATE utf8mb4_unicode_ci,
  `hazard_chem` int(1) NOT NULL DEFAULT '0',
  `competent_to_work` varchar(140) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `demolition` int(1) NOT NULL DEFAULT '0',
  `safe_work` varchar(140) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `earmuffs` int(1) NOT NULL DEFAULT '0',
  `permit_start_date` datetime(6) DEFAULT NULL,
  `safety_footwear` int(1) NOT NULL DEFAULT '0',
  `other_tasks` int(1) NOT NULL DEFAULT '0',
  `amended_from` varchar(140) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `fail_arrest_restraint` int(1) NOT NULL DEFAULT '0',
  `hearing_protection` int(1) NOT NULL DEFAULT '0',
  `over_2m` int(1) NOT NULL DEFAULT '0',
  `work_in_areas_near_members_of_the_public` int(1) NOT NULL DEFAULT '0',
  `hot_work` int(1) NOT NULL DEFAULT '0',
  `incident_occur_severity` varchar(140) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `company_name` varchar(140) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `scope` varchar(140) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `insurance_assessment` varchar(140) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `likely_incident` varchar(140) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `location` varchar(140) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `others_task` text COLLATE utf8mb4_unicode_ci,
  `gloves_and_other_hand_protection` int(1) NOT NULL DEFAULT '0',
  `work_in_high_production_areas` int(1) NOT NULL DEFAULT '0',
  `approver` varchar(140) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `_user_tags` text COLLATE utf8mb4_unicode_ci,
  `relevent_training` varchar(140) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `other_equipment` text COLLATE utf8mb4_unicode_ci,
  `asbestos` int(1) NOT NULL DEFAULT '0',
  `high_visible_clothing` int(1) NOT NULL DEFAULT '0',
  `eye_face_protection` int(1) NOT NULL DEFAULT '0',
  `respiratory_protection` int(1) NOT NULL DEFAULT '0',
  `_assign` text COLLATE utf8mb4_unicode_ci,
  `_comments` text COLLATE utf8mb4_unicode_ci,
  `window_cleaning` int(1) NOT NULL DEFAULT '0',
  `near_elect` int(1) NOT NULL DEFAULT '0',
  `barriers_sign` int(1) NOT NULL DEFAULT '0',
  `certifications_task` varchar(140) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `mobile_plant` int(1) NOT NULL DEFAULT '0',
  `using_power_tools` int(1) NOT NULL DEFAULT '0',
  `abrasive_blasting` int(1) NOT NULL DEFAULT '0',
  `authorized_by` varchar(140) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `permit_number` varchar(140) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `hard_hats` int(1) NOT NULL DEFAULT '0',
  `confined_space_entry` int(1) NOT NULL DEFAULT '0',
  `permit_completion_date` datetime(6) DEFAULT NULL,
  `workflow_state` varchar(140) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=COMPRESSED;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tabContractor Permit to Work`
--

LOCK TABLES `tabContractor Permit to Work` WRITE;
/*!40000 ALTER TABLE `tabContractor Permit to Work` DISABLE KEYS */;
INSERT INTO `tabContractor Permit to Work` VALUES ('GCL-CWP-001','2017-08-24 15:05:12.798827','2017-08-26 13:43:14.263020','ese.egbevwie@graceco.com.ng','Administrator',1,NULL,NULL,NULL,2,1,'GCL-EMP/0100',0,'Ese Egbevwie',0,0,'Injury, eye disorder.',NULL,0,'Yes',0,'No',0,'2017-08-21 00:00:00.000000',1,0,NULL,0,0,0,0,1,'Serious injury or moderate damage','Fasco Construction','Welding','No','Possible','Bakery',NULL,1,0,'Shola.amao@graceco.com.ng',NULL,'Yes','Not all the necessary PPE  was provided for this work.',0,0,1,0,NULL,'[{\"comment\": \"Not all the necessary  PPE was provided for this job. Only eye protector was provided.\", \"by\": \"ese.egbevwie@graceco.com.ng\", \"name\": \"1702f4554a\"}]',0,0,0,'Yes',0,0,0,'ese.egbevwie@graceco.com.ng',NULL,1,0,'2017-08-22 00:00:00.000000','Permitted'),('GCL-CWP-002','2017-08-28 15:58:24.568827','2017-08-28 17:12:34.185035','ese.egbevwie@graceco.com.ng','ese.egbevwie@graceco.com.ng',1,NULL,NULL,NULL,2,0,'GCL-EMP/0100',0,'Ese Egbevwie',0,0,'Serious/fatal injury as a result of falling from height.',NULL,0,'Yes',0,'No',0,'2017-08-28 15:41:28.000000',1,0,NULL,1,0,1,1,0,'Death or major damage','Sammy Furniture','Repair of Roof','Yes','Possible','laboratory',NULL,1,0,'bayo.ayoade@graceco.com.ng',NULL,'Yes','Not all the necessary PPE was provided for this task.',0,1,0,0,NULL,'[{\"comment\": \"Only hard hat is available PPE\", \"by\": \"ese.egbevwie@graceco.com.ng\", \"name\": \"3f0549ea07\"}]',0,0,0,'Yes',0,0,0,'ese.egbevwie@graceco.com.ng',NULL,1,0,'2017-08-28 16:21:25.000000','Permitted'),('GCL-CWP-003','2017-08-30 11:39:22.891410','2017-08-30 12:25:05.583078','ese.egbevwie@graceco.com.ng','ese.egbevwie@graceco.com.ng',0,NULL,NULL,NULL,0,1,'GCL-EMP/0100',0,'Ese Egbevwie',0,0,'Injury and eye disorder',NULL,0,'Yes',0,'No',0,'2017-08-30 11:36:11.000000',1,0,NULL,0,0,0,1,1,'Serious injury or moderate damage','Fasco Construction and Fabrication','Fabricating and erection work','Yes','Possible','Chinchin',NULL,1,0,'Shola.amao@graceco.com.ng',NULL,'Yes','Not all the necessary PPE is provided.',0,0,1,0,NULL,NULL,0,0,0,'Yes',0,0,0,'ese.egbevwie@graceco.com.ng',NULL,1,0,NULL,'Draft'),('GCL-CWP-004','2017-08-30 12:22:24.898641','2017-08-30 12:22:24.898641','ese.egbevwie@graceco.com.ng','ese.egbevwie@graceco.com.ng',0,NULL,NULL,NULL,0,1,'GCL-EMP/0100',0,'Ese Egbevwie',0,0,'Injury and eye disorder',NULL,0,'Yes',0,'No',1,'2017-08-30 11:36:11.000000',1,0,NULL,0,0,0,1,1,'Minor injury or damage','Fasco Construction and Fabrication','Fabrication and erection','Yes','Unlikely','Bakery',NULL,1,0,'Shola.amao@graceco.com.ng',NULL,'Yes','Not all the necessary PPE is provided.',0,0,1,0,NULL,NULL,0,0,0,'Yes',0,0,0,'ese.egbevwie@graceco.com.ng',NULL,1,0,NULL,'Draft'),('GCL-CWP-005','2017-08-30 13:01:11.537640','2017-08-31 16:23:26.399525','ese.egbevwie@graceco.com.ng','ese.egbevwie@graceco.com.ng',0,NULL,NULL,NULL,0,0,'GCL-EMP/0100',0,'Ese Egbevwie',1,0,'Injury: Falling from height,eye disorder, electrical shock.',NULL,0,'Yes',1,'Yes',0,'2017-08-30 11:36:11.000000',1,0,NULL,1,0,0,1,1,'Minor injury or damage','AJKEG ENGINEERING COMPANY','Duct installation','No','Unlikely','Chinchin',NULL,1,1,'',NULL,'Yes',NULL,0,1,1,0,NULL,NULL,0,1,0,'Yes',0,0,0,'ese.egbevwie@graceco.com.ng',NULL,1,0,NULL,'Draft'),('GCL-CWP-006','2017-08-31 13:54:07.989982','2017-08-31 13:54:07.989982','ese.egbevwie@graceco.com.ng','ese.egbevwie@graceco.com.ng',0,NULL,NULL,NULL,0,0,'GCL-EMP/0100',0,'Ese Egbevwie',0,0,'Falling from height.',NULL,0,'Yes',0,'No',0,'2017-08-31 13:47:47.000000',1,0,NULL,1,0,1,1,0,'Serious injury or moderate damage','Samcool','Relocation of AC, re-installation and servicing of AC','No','Possible','Bakery',NULL,1,1,'Shola.amao@graceco.com.ng',NULL,'Yes','Not all the necessary PPE is provided.',0,1,0,0,NULL,NULL,0,0,0,'Yes',0,0,0,'ese.egbevwie@graceco.com.ng',NULL,1,0,NULL,'Draft');
/*!40000 ALTER TABLE `tabContractor Permit to Work` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-09-05 12:19:52
