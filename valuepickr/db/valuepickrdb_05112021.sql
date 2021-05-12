CREATE DATABASE  IF NOT EXISTS `valuepickrdb` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `valuepickrdb`;
-- MySQL dump 10.13  Distrib 8.0.24, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: valuepickrdb
-- ------------------------------------------------------
-- Server version	8.0.24

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `topic`
--

DROP TABLE IF EXISTS `topic`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `topic` (
  `TopicId` int NOT NULL AUTO_INCREMENT,
  `TopicName` varchar(200) DEFAULT NULL,
  `TopicURL` varchar(200) DEFAULT NULL,
  `CreatedDate` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`TopicId`)
) ENGINE=InnoDB AUTO_INCREMENT=376 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topic`
--

LOCK TABLES `topic` WRITE;
/*!40000 ALTER TABLE `topic` DISABLE KEYS */;
INSERT INTO `topic` VALUES (279,'Prakash Pipes and Fittings (PPL) - Not just Pipes','https://forum.valuepickr.com/t/prakash-pipes-and-fittings-ppl-not-just-pipes/56047','2021-05-09 22:54:08'),(280,'Nitin Spinner - textile yarn story','https://forum.valuepickr.com/t/nitin-spinner-textile-yarn-story/212/165','2021-05-09 22:54:08'),(281,'Vedanta Limited - Future Natural Resource Leader','https://forum.valuepickr.com/t/vedanta-limited-future-natural-resource-leader/14634/134','2021-05-09 22:54:08'),(282,'Indiamart Intermesh - Indian Alibaba?','https://forum.valuepickr.com/t/indiamart-intermesh-indian-alibaba/23734/250','2021-05-09 22:54:08'),(283,'Fine Organics - Niche Player in Specialty Chemical','https://forum.valuepickr.com/t/fine-organics-niche-player-in-specialty-chemical/18411/27','2021-05-09 22:54:08'),(284,'Kama Holdings Limited','https://forum.valuepickr.com/t/kama-holdings-limited/2335/17','2021-05-09 22:54:08'),(285,'Pix transmissions - low profile microcap company','https://forum.valuepickr.com/t/pix-transmissions-low-profile-microcap-company/3872/113','2021-05-09 22:54:08'),(286,'Caplin Point Laboratories','https://forum.valuepickr.com/t/caplin-point-laboratories/948/622','2021-05-09 22:54:08'),(287,'CreditAccess Grameen: Traditional MFI model, efficiently operating at scale','https://forum.valuepickr.com/t/creditaccess-grameen-traditional-mfi-model-efficiently-operating-at-scale/30007/15','2021-05-09 22:54:08'),(288,'Deepak Nitrite','https://forum.valuepickr.com/t/deepak-nitrite/977/349','2021-05-09 22:54:09'),(289,'Navin Flourine International','https://forum.valuepickr.com/t/navin-flourine-international/1691/43','2021-05-09 22:54:09'),(290,'Acrysil - Kitchen sinks','https://forum.valuepickr.com/t/acrysil-kitchen-sinks/1060/106','2021-05-09 22:54:09'),(291,'Neogen Chemicals - Niche player in specialty chemicals','https://forum.valuepickr.com/t/neogen-chemicals-niche-player-in-specialty-chemicals/40293/13','2021-05-09 22:54:09'),(292,'Godawari Power - Any Trackers?','https://forum.valuepickr.com/t/godawari-power-any-trackers/4815/113','2021-05-09 22:54:09'),(293,'Transpek Industry limited','https://forum.valuepickr.com/t/transpek-industry-limited/6380/189','2021-05-09 22:54:09'),(294,'Intellect Design Arena','https://forum.valuepickr.com/t/intellect-design-arena/1228/237','2021-05-09 22:54:09'),(295,'Palred technologies - www.latestone.com','https://forum.valuepickr.com/t/palred-technologies-www-latestone-com/1435/22','2021-05-09 22:54:09'),(296,'Mohini Health and Hygiene','https://forum.valuepickr.com/t/mohini-health-and-hygiene/52255/9','2021-05-09 22:54:09'),(297,'Himachal Futuristic communication','https://forum.valuepickr.com/t/himachal-futuristic-communication/13032/77','2021-05-09 22:54:09'),(298,'DHP India Ltd - Regulators and Fittings','https://forum.valuepickr.com/t/dhp-india-ltd-regulators-and-fittings/1858/125','2021-05-09 22:54:09'),(299,'KRBL- The King of Basmati rice','https://forum.valuepickr.com/t/krbl-the-king-of-basmati-rice/1045/962','2021-05-09 22:54:09'),(300,'SastaSundar Ventures Ltd (a new venture in the nascent epharmacy space)','https://forum.valuepickr.com/t/sastasundar-ventures-ltd-a-new-venture-in-the-nascent-epharmacy-space/8780/38','2021-05-09 22:54:10'),(301,'Kanchi Karpooram Ltd','https://forum.valuepickr.com/t/kanchi-karpooram-ltd/21621/91','2021-05-09 22:54:10'),(302,'Lincoln Pharma … the next mid-cap pharma in the making …?','https://forum.valuepickr.com/t/lincoln-pharma-the-next-mid-cap-pharma-in-the-making/3294/140','2021-05-09 22:54:10'),(303,'WPIL Ltd - Global Water Pumps','https://forum.valuepickr.com/t/wpil-ltd-global-water-pumps/19040/27','2021-05-09 22:54:10'),(304,'Paper Felts & Fabrics– A Subscription Opportunity in the Old Analog World','https://forum.valuepickr.com/t/paper-felts-fabrics-a-subscription-opportunity-in-the-old-analog-world/55248','2021-05-09 22:54:10'),(305,'Chaman Lal Setia Exports Ltd (CLSE)','https://forum.valuepickr.com/t/chaman-lal-setia-exports-ltd-clse/2560/190','2021-05-09 22:54:10'),(306,'HLE Glascoat - (Valuation gap with GMM Pfaudler)?','https://forum.valuepickr.com/t/hle-glascoat-valuation-gap-with-gmm-pfaudler/6104/60','2021-05-09 22:54:10'),(307,'Valiant Organics - High ROCE, debt free','https://forum.valuepickr.com/t/valiant-organics-high-roce-debt-free/9088/277','2021-05-09 22:54:10'),(308,'Sadhana nitro :a Dog or a Horse?','https://forum.valuepickr.com/t/sadhana-nitro-a-dog-or-a-horse/17791/111','2021-05-09 22:54:10'),(309,'Time technoplast','https://forum.valuepickr.com/t/time-technoplast/6463/80','2021-05-09 22:54:10'),(310,'NILE Limited-Lead Supplier','https://forum.valuepickr.com/t/nile-limited-lead-supplier/12093/8','2021-05-09 22:54:11'),(311,'Gujarat Themis Biosyn Ltd - Bulk Drugs growth momentum','https://forum.valuepickr.com/t/gujarat-themis-biosyn-ltd-bulk-drugs-growth-momentum/36594/81','2021-05-09 22:54:11'),(312,'Som Distilleries and Breweries','https://forum.valuepickr.com/t/som-distilleries-and-breweries/16821/67','2021-05-09 22:54:11'),(313,'IOLCP - Synergy in operations made monopoly in product integration','https://forum.valuepickr.com/t/iolcp-synergy-in-operations-made-monopoly-in-product-integration/11412/471','2021-05-09 22:54:11'),(314,'S.H. Kelkar Ltd','https://forum.valuepickr.com/t/s-h-kelkar-ltd/3236/64','2021-05-09 22:54:11'),(315,'Meghmani Organics Ltd','https://forum.valuepickr.com/t/meghmani-organics-ltd/1257/377','2021-05-09 22:54:11'),(316,'KPIT anyone?','https://forum.valuepickr.com/t/kpit-anyone/289/109','2021-05-09 22:54:12'),(317,'POKARNA LTD ( Stock opportunities )','https://forum.valuepickr.com/t/pokarna-ltd-stock-opportunities/1863/716','2021-05-09 22:54:12'),(318,'Route Mobile - Internet, Mobile & Telecom','https://forum.valuepickr.com/t/route-mobile-internet-mobile-telecom/43077/83','2021-05-09 22:54:12'),(319,'Affle India - India Mobile Internet Advertising Leader','https://forum.valuepickr.com/t/affle-india-india-mobile-internet-advertising-leader/24230/246','2021-05-09 22:54:12'),(320,'Ultramarine & Pigments','https://forum.valuepickr.com/t/ultramarine-pigments/2427/120','2021-05-09 22:54:12'),(321,'Kothari fermentation & biochem ltd','https://forum.valuepickr.com/t/kothari-fermentation-biochem-ltd/5556/23','2021-05-09 22:54:12'),(322,'Gulshan Polyols(GPL) - Business by FMCG and Valuation by Commodity','https://forum.valuepickr.com/t/gulshan-polyols-gpl-business-by-fmcg-and-valuation-by-commodity/2217/72','2021-05-09 22:54:13'),(323,'Wonderla Holidays','https://forum.valuepickr.com/t/wonderla-holidays/1053/486','2021-05-09 22:54:13'),(324,'Ganesh Benzoplast - Cash rich chemical storage/tank king','https://forum.valuepickr.com/t/ganesh-benzoplast-cash-rich-chemical-storage-tank-king/9894/147','2021-05-09 22:54:13'),(325,'PPAP automotive ltd','https://forum.valuepickr.com/t/ppap-automotive-ltd/5192/70','2021-05-09 22:54:13'),(326,'Jash Engineering - Is it a multibagger','https://forum.valuepickr.com/t/jash-engineering-is-it-a-multibagger/13743/32','2021-05-09 22:54:13'),(327,'InfoBeans Ltd - IT Solid Growth Story','https://forum.valuepickr.com/t/infobeans-ltd-it-solid-growth-story/22630/25','2021-05-09 22:54:13'),(328,'Ice make Refrigeration - Picks & shovels for cold storage infrastructure','https://forum.valuepickr.com/t/ice-make-refrigeration-picks-shovels-for-cold-storage-infrastructure/18642/34','2021-05-09 22:54:14'),(329,'Suven Pharma ~ Demerged CRAMS Arm of Suven Life Sciences','https://forum.valuepickr.com/t/suven-pharma-demerged-crams-arm-of-suven-life-sciences/221/370','2021-05-09 22:54:14'),(330,'Safari Industries (India) Ltd','https://forum.valuepickr.com/t/safari-industries-india-ltd/5763/160','2021-05-09 22:54:14'),(331,'Johnson Controls- Hitachi India Pvt Limited','https://forum.valuepickr.com/t/johnson-controls-hitachi-india-pvt-limited/34274/18','2021-05-09 22:54:14'),(332,'Hester Biosciences - Growing Steadily','https://forum.valuepickr.com/t/hester-biosciences-growing-steadily/1029/159','2021-05-09 22:54:14'),(333,'HealthCare Global – the value unlocking story','https://forum.valuepickr.com/t/healthcare-global-the-value-unlocking-story/17065/49','2021-05-09 22:54:14'),(334,'Intense Technologies','https://forum.valuepickr.com/t/intense-technologies/7155/309','2021-05-09 22:54:15'),(335,'Heidelberg Cement India Ltd.- With all boxes ticking, can it deliver?','https://forum.valuepickr.com/t/heidelberg-cement-india-ltd-with-all-boxes-ticking-can-it-deliver/33238/7','2021-05-09 22:54:15'),(336,'MIDHANI : Niche high valued added domestic alloy company','https://forum.valuepickr.com/t/midhani-niche-high-valued-added-domestic-alloy-company/27073/16','2021-05-09 22:54:15'),(337,'Marksans Pharma- Can it be the next Pharma Biggie?','https://forum.valuepickr.com/t/marksans-pharma-can-it-be-the-next-pharma-biggie/1520/120','2021-05-09 22:54:15'),(338,'Associated alcholols & breweries ltd','https://forum.valuepickr.com/t/associated-alcholols-breweries-ltd/1570/137','2021-05-09 22:54:15'),(339,'Asahi Songwon - Steady Performer','https://forum.valuepickr.com/t/asahi-songwon-steady-performer/2296/24','2021-05-09 22:54:15'),(340,'Chemcrux Enterprises - A dark horse?','https://forum.valuepickr.com/t/chemcrux-enterprises-a-dark-horse/18006/146','2021-05-09 22:54:16'),(341,'Dai-Ichi Karkaria Limited','https://forum.valuepickr.com/t/dai-ichi-karkaria-limited/937/149','2021-05-09 22:54:16'),(342,'Tanla Solutions - a niche player in m-commerce space and a turn around story?','https://forum.valuepickr.com/t/tanla-solutions-a-niche-player-in-m-commerce-space-and-a-turn-around-story/3356/46','2021-05-09 22:54:16'),(343,'GTPL Hathway Limited','https://forum.valuepickr.com/t/gtpl-hathway-limited/20054/23','2021-05-09 22:54:16'),(344,'Vaibhav Global : Back from the dead','https://forum.valuepickr.com/t/vaibhav-global-back-from-the-dead/960/371','2021-05-09 22:54:16'),(345,'Jasch Industries Ltd - value unlocking possible?','https://forum.valuepickr.com/t/jasch-industries-ltd-value-unlocking-possible/7979/5','2021-05-09 22:54:16'),(346,'Banka BioLoo Limited','https://forum.valuepickr.com/t/banka-bioloo-limited/52291/5','2021-05-09 22:54:16'),(347,'Sterlite Technologies | Digital India play','https://forum.valuepickr.com/t/sterlite-technologies-digital-india-play/3473/470','2021-05-09 22:54:17'),(348,'Sonata Software A Turnaround Story','https://forum.valuepickr.com/t/sonata-software-a-turnaround-story/969/127','2021-05-09 22:54:17'),(349,'Xelpmoc Design and Tech Ltd','https://forum.valuepickr.com/t/xelpmoc-design-and-tech-ltd/43305/80','2021-05-09 22:54:17'),(350,'Precision Camshafts','https://forum.valuepickr.com/t/precision-camshafts/13990/30','2021-05-09 22:54:17'),(351,'Shree Pushkar Chemicals','https://forum.valuepickr.com/t/shree-pushkar-chemicals/8385/205','2021-05-09 22:54:17'),(352,'Khaitan Chemicals & Fertilizers Ltd. - Achhe Din in store!','https://forum.valuepickr.com/t/khaitan-chemicals-fertilizers-ltd-achhe-din-in-store/42679/22','2021-05-09 22:54:18'),(353,'Krebs Biochemicals & Industries - can it be one of the next pharma multibagger?','https://forum.valuepickr.com/t/krebs-biochemicals-industries-can-it-be-one-of-the-next-pharma-multibagger/3623/5','2021-05-09 22:54:18'),(354,'Shivalik Bimetal Controls Ltd','https://forum.valuepickr.com/t/shivalik-bimetal-controls-ltd/16938/162','2021-05-09 22:54:18'),(355,'VLS Finance limited (511333)','https://forum.valuepickr.com/t/vls-finance-limited-511333/207/66','2021-05-09 22:54:18'),(356,'Premco Global — Narrow Fabric (A critical component for inner wear)','https://forum.valuepickr.com/t/premco-global-narrow-fabric-a-critical-component-for-inner-wear/1341/375','2021-05-09 22:54:18'),(357,'Amrutanjan Healthcare - Finally Waking Up After 100 years?','https://forum.valuepickr.com/t/amrutanjan-healthcare-finally-waking-up-after-100-years/3531/57','2021-05-09 22:54:18'),(358,'Solex Energy - Undervalued Solar PV Manufacturer or Microcap Value Trap?','https://forum.valuepickr.com/t/solex-energy-undervalued-solar-pv-manufacturer-or-microcap-value-trap/53512/8','2021-05-09 22:54:18'),(359,'INEOS Styrolution India Ltd','https://forum.valuepickr.com/t/ineos-styrolution-india-ltd/3132/43','2021-05-09 22:54:19'),(360,'Paushak Ltd. - Alembic’s agrochemical business','https://forum.valuepickr.com/t/paushak-ltd-alembics-agrochemical-business/1517/211','2021-05-09 22:54:19'),(361,'Granules India Ltd','https://forum.valuepickr.com/t/granules-india-ltd/940/1272','2021-05-09 22:54:19'),(362,'Solar Industries Ltd','https://forum.valuepickr.com/t/solar-industries-ltd/211/68','2021-05-09 22:54:19'),(363,'20 Microns - potential multibagger','https://forum.valuepickr.com/t/20-microns-potential-multibagger/17686/21','2021-05-09 22:54:19'),(364,'Happiest Minds Technology','https://forum.valuepickr.com/t/happiest-minds-technology/46478/7','2021-05-09 22:54:19'),(365,'Pulz Electronics - proxy to the Indian entertainment sector','https://forum.valuepickr.com/t/pulz-electronics-proxy-to-the-indian-entertainment-sector/23828/5','2021-05-09 22:54:19'),(366,'Rossari Biotech Ltd - Can growth justify expensive valuation?','https://forum.valuepickr.com/t/rossari-biotech-ltd-can-growth-justify-expensive-valuation/37904/36','2021-05-09 22:54:20'),(367,'V-Mart Retail Ltd','https://forum.valuepickr.com/t/v-mart-retail-ltd/988/225','2021-05-09 22:54:20'),(368,'NOCIL Limited ~ One-Stop-Shop for Rubber Chemicals in India','https://forum.valuepickr.com/t/nocil-limited-one-stop-shop-for-rubber-chemicals-in-india/6206/204','2021-05-09 22:54:20'),(369,'Parag Milk Foods - FMCG company just in Name or Deed?','https://forum.valuepickr.com/t/parag-milk-foods-fmcg-company-just-in-name-or-deed/4163/293','2021-05-09 22:54:20'),(370,'NGL Fine-Chem (Animal Health + Human Health + Vet Formulations)','https://forum.valuepickr.com/t/ngl-fine-chem-animal-health-human-health-vet-formulations/2276/210','2021-05-09 22:54:20'),(371,'The Anup Engineering Ltd - Can it scale up?','https://forum.valuepickr.com/t/the-anup-engineering-ltd-can-it-scale-up/23078/72','2021-05-09 22:54:20'),(372,'Oriental Aromatics (Earlier: Camphor & Allied Products Ltd)','https://forum.valuepickr.com/t/oriental-aromatics-earlier-camphor-allied-products-ltd/8379/45','2021-05-11 13:04:46'),(373,'Nureca - Online Distribution Of Home Healthcare Products','https://forum.valuepickr.com/t/nureca-online-distribution-of-home-healthcare-products/56154','2021-05-11 13:04:46'),(374,'Prakash Pipes and Fittings (PPFL) - Not just Pipes','https://forum.valuepickr.com/t/prakash-pipes-and-fittings-ppfl-not-just-pipes/56047','2021-05-11 13:04:47'),(375,'Varroc Engineering Ltd','https://forum.valuepickr.com/t/varroc-engineering-ltd/21748/36','2021-05-11 13:04:47');
/*!40000 ALTER TABLE `topic` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topiccategory`
--

DROP TABLE IF EXISTS `topiccategory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `topiccategory` (
  `TopicCategoryId` int NOT NULL AUTO_INCREMENT,
  `TopicId` int DEFAULT NULL,
  `CategoryName` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`TopicCategoryId`),
  KEY `TopicId` (`TopicId`),
  CONSTRAINT `topiccategory_ibfk_1` FOREIGN KEY (`TopicId`) REFERENCES `topic` (`TopicId`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topiccategory`
--

LOCK TABLES `topiccategory` WRITE;
/*!40000 ALTER TABLE `topiccategory` DISABLE KEYS */;
INSERT INTO `topiccategory` VALUES (2,279,'Stock Opportunities'),(3,279,'Untested - but worth a good look');
/*!40000 ALTER TABLE `topiccategory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topicdiscussion`
--

DROP TABLE IF EXISTS `topicdiscussion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `topicdiscussion` (
  `TopicDiscussionId` int NOT NULL AUTO_INCREMENT,
  `TopicId` int DEFAULT NULL,
  `UserId` int DEFAULT NULL,
  `DiscussionText` text,
  `DiscussionDate` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`TopicDiscussionId`),
  KEY `TopicId` (`TopicId`),
  KEY `UserId` (`UserId`),
  CONSTRAINT `topicdiscussion_ibfk_1` FOREIGN KEY (`TopicId`) REFERENCES `topic` (`TopicId`),
  CONSTRAINT `topicdiscussion_ibfk_2` FOREIGN KEY (`UserId`) REFERENCES `user` (`UserId`)
) ENGINE=InnoDB AUTO_INCREMENT=99 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topicdiscussion`
--

LOCK TABLES `topicdiscussion` WRITE;
/*!40000 ALTER TABLE `topicdiscussion` DISABLE KEYS */;
INSERT INTO `topicdiscussion` VALUES (92,279,1,'Hi,\nThis is my first writeup on VP, so consider any lapses kindly. I will keep the writeup short, and based on questions or conversations, attempt to find and update related information.\nI wish to draw attention to a small scale regional player in plastic pipes - Prakash Pipes- PPFL.\nPrimary investment thesis - A subsidiary business with impressive performance while the primary business is likely to benefit from the tailwinds in the plastic pipes space.\nBusiness history - Primary promoter in business since 1981. Initially part of Prakash industries which also has interests in steel, power and mining (Refer thread on Prakash Industries on VP). PVC pipes and plastics division demerged out in 2019 into separate entity with investors getting shares in ratio 8:1. (for 8 in parent, get 1 in new). Company starts trading on BSE/NSE as separate entity from June, 2019.\nCurrent Business - Initially, as part of Prakash industries, PPFL was primarily a plastic pipes company. While plastic pipes industry faces reasonable tailwinds in the business today, Prakash pipes is relatively small and decent regional player in the north (UP primarily and then the Delhi, Haryana and Northwards belt, with influence gradually diminishing as we move north east or south). In 2018, however, PPFL diversified into the flexible packaging space. The key attractiveness of the business lies in the flexible packaging division which is growing at an incredible rate.\nThe story in numbers is as follows -\nParticulars FY19 FY20 9MFY21\nTotal Revenue 345.6 389.2 342.4\nEBITDA 43.2 42.4 43.6\nEBITDA margin (%) 12.50% 10.90% 12.70%\nDepreciation 4.7 6.5 6\nInterest 0.2 1.6 1.5\nProfit Before Tax 38.3 34.3 36.2\nIncome Tax 9.7 9.5 10.5\nProfit After Tax 28.6 24.8 25.6\nPAT margin (%) 8.30% 6.40% 7.50%\nSales Volume (MTPA) FY19 FY20 9MFY21\nPipes & Fittings 42,012 43,305 28,025\nFlexible Packaging 316 3,227 5,227\nCurrent year highlights (Q3 - Fy2021)\nQuarter Ended Dec, 2020\nRevenue - INR 127 Crores, up by 37% (YoY)\nEBITDA - INR 16 Crores, up by 63% (YoY)\nProfit After Tax - INR 9 Crores, up by 25% (YoY)\n9 Months Ended Dec, 2020\nRevenue - INR 342 Crores, up by 14% (YoY)\nEBITDA - INR 44 Crores, up by 34% (YoY)\nProfit After Tax - INR 26 Crores, up by 25% (YoY)\nPipes & Fittings Division\nRecorded sales volume of 10,013 tonnes in Q3FY21, up by 4% (YoY)\nContribution of the Fittings in the sales mix has increased to 7%, up by 83% (YoY)\nInstalled 3 new Moulding machines to expand the Fittings range\nAdded Chlorinated Polyvinyl Chloride (CPVC) Pipes & Fittings in the product range\nFlexible Packaging Division\nSales volume grew by 60% (YoY) in Q3FY21\nIncreased capacity by commissioning 3rd Printing Machine\nCommissioned Rotogravure Cylinder plant as a step towards backward integration\nIncremental planned Capex - Company is planning significant further Capex in both its divisions, as of now, all funded through internal accruals.\nCapex Current Target FY21/22 Percent Increase\nPipes & Fittings 55000 TPA 67000 TPA 22%\nFlexible Packaging 9600 TPA 19200 TPA 100%\nIt is interesting to note that flexible packaging incremental capex is comparable (12000 TPA to 9600 TPA) to its long standing pipes division in absolute terms, while in percentage terms absolutely blows the pipes capex out of the water (at 22pc vs 100 pc that’s a no-contest really) and in my opinion indicative of where the management thinks future profits will be from.\nFrom screener, With ROCE at healthy 29%, EPS of 14, P/E of 10, and debt-free, it seems pretty fairly valued with respect to its pipes competitions as well as packaging competition.\nShort Business Note - Pipes\nCurrent plant at Kashipur UP.\n500+ dealer and distributor network\nfavorable tailwinds with consolidation in pipes industry and Jal Jeevan Mission, Krishi Sinchayee Yojana and Pradhan Mantri Awaas Yojana.\nFor a fuller discussion of the pipes industry please check this link - https://www.valuequest.in/deep-dive-series-plastic-pipes/ 10\nShort Business Note - Flexible Packaging -\nagain, plant at Kashipur UP.\nbackward integration with printing inks, blown PE films and Rotogravure cylinders.\nvery healthy client list with repeat business across FMCG, food and Infrastructure/Others.\nOverall, company looks favorably poised to benefit from the pipe industry tailwinds, with the flexible packaging division serving as the cherry on the pie. At current prices and valuations, looks like there is significant upside to the stock, even after the nearly 5x runup over the last year.\nViews/questions/opinions invited from esteemed members of this forum.\nDisclosure: Invested and accumulating.\nEdit 1 : Apparently, RJ is invested in this from lower levels.\nEdit 2: In response to Sahil’s questions below. Have added what I think are the key risks as well as links and pointers to more information (as much as I could find).\nKey risks\nPVC resin imports is the most significant raw material needed. India imports 56% of its PVC resin needs. Larger players have better cost efficiencies in procurement. Not sure where PPFL stands in this regard. PVC resin import also has ADD (Anti Dumping Duty) applicable, but again, whether that’s a good thing or bad thing for smaller players is subjective based on costs involved for the player and the ability to pass the cost downwards to its customers…\nPromoter risk - Prakash Industries, the founding company, is involved in lawsuits filed by CBI against certain operations of its mining businesses.\nBusiness and prospects details -\nPipes - the value quest article above is a good starting point. It has several details about the process, the inputs, the market segmentation and the overall industry business prospects.\nFlexible Packaging - the best source of information I could find was this pdf presentation by Dr Ranweer Alam, Director, IIP (Indian Institute of Packaging). http://missp.ch/docs/1590652928The%20Indian%20Packaging%20Industry%20-%20Post%20Covid-19%20as%20an%20Opportunities%20in%20Packaging%20Business.pdf 4. Most other articles and research reports are behind a paywall.\nOther links\nIndian Packaging Industry Riding On The E-commerce Wave | IBEF | IBEF 2,\nCovid-19: Packaging industry sees higher volume growth in June-qtr | Business Standard News\nPackaging Market in India 2020-2024 | Shift Toward the Use of Flexible Packaging to Boost Market Growth | Technavio | Business Wire\nPacking industry holds potential for high growth - The Hindu BusinessLine 1\nThe India Packaging Market was valued at USD 50.5 billion\nThe Annual report of the company is a very good read. The overviews of the business landscape, both overall and division wise are excellent. The rest of it is also eminently readable, unlike most, where you actually have to push through.\nIn addition, one other point, although minor, does make a good impression. Both the annual report, and the site, are among the most polished of any small business I have seen. The Annual report is excellent in terms of its readability, while the web-site is slick and fast.\nWeb-site - https://prakashplastics.in/ 3\nAnnual report link - Annual Report | Prakash Pipes Limited','May 9, 2021 10:37 pm'),(93,279,2,'Hi blue,\nI absolutely love your post and it has forced me to evaluate this business. Would like to add that all first posts about a business must include key risks section mandatorily. Without that some moderator will end up locking this thrrad.\nCan you please add a small section in the first post on the key risks presented in the business and the company/investment so that investors get a balanced viewpoint from first post itself.\nIn terms of digging deeper this is a noob question but can you please describe what both the divisions do (what products or services do they provide?). If you could share links to these sections on their website or small writeups on the products or services provided under both the divisions that would be great too. If you are unable to do so that any reason, no worries. I’m sure someone else (which might very well end up being me because I am excited to study this business soon) will take up the mantle and post answers to these basic questions about what are the goods or services provided in each segment. What is flexible packaging? What are cpvc pipes ?\nAgain, thanks for starting this thread.','May 10, 2021 12:30 am'),(94,279,1,'Hi Sahil,\nThanks for the response. Having read some of your analysis on other threads, I will be keenly waiting for your findings.\nW.r.t your questions, have added a key risks section as well as some pointers to the different industry segments. This, more or less, encompasses most of what I know so far.\nCertain details like what fraction of the flexible packaging is in repeat business, what are the shares of the highest clients are not available. I would have liked to get those from somewhere. But overall, my sense of risk here is not high. The worst, imho, is that the main growth phase is past and we may not see a significant up move from here on, but it does not look like that for me, especially considering the significant investments into capex (both divisions), and the diversification of pipes into CPVC from PVC and the added focus on fittings, it seems that the firm is gearing up well to tackle competition in its home grounds at least (pipes division).\nThe next few quarters performance should be quite enlightening though.\nOn a separate note - congratulations on successfully kicking the sh*t out of C19. No doubt it was a most miserable experience, but you are now out on the other end, and looking at the brighter side, you don’t have to queue up for the miraculously unavailable vaccines, not for a few months at least.','May 10, 2021 1:55 am'),(95,279,2,'Open ED and CBI cases against promoter entities\nblue:\nPromoter risk - Prakash Industries, the founding company, is involved in lawsuits filed by CBI against certain operations of its mining businesses\nI Quote from following 2018 article 1:\nED article:\nThe ED investigation revealed that as a result of the false ‘filing’, share prices of Prakash Industries jumped 10 times from Rs 31 on 2 April 2007 to Rs 351 on 4 January 2008. The investigation further revealed that to take advantage of the ‘artificially created rise in the share value’, the company issued 62,50,000 preferential shares on a premium of Rs 180 per share and sold these shares to five companies making a gain of 118.75 crores.\n“The amount of Rs 118.75 crores, which was generated as a result of the schedule offence as committed on the date of filing of application for allocation of coal block by giving false net worth details and further false declaration to BSE, is the proceeds of crime, which are liable to be provisionally attached under PMLA,” says a media statement by Enforcement Directorate.\nI quote from a similar 2021 article 2:\nCBI Article:\nThe CBI has sought government’s permission to charge three bureaucrats, two of whom are retired, in a coal scam case they had closed for want of evidence, but reopened based on application by senior BJP leaders, also complainants in case.\nThe CBI had filed a case against Prakash Industries and its directors in 2014 on the complaints of Union Minister Prakash Javdekar and senior BJP leaders Hans Raj Ahir and Bhupender Yadav.\nThe three BJP leaders, being the complainants, had opposed the closure report in the CBI court and sought further investigation, which the CBI agreed to on March 9, 2018.\nAs per the ED article The promoters have been involved directly in wrong filings with exchanges leading to stock price manipulation. As per the CBI article there are political risks as well with some tussle between leaders of ruling party. IMO the promoter entity related risks are far too high. Specially in a microcap like prakash where most information is already opaque (no concalls), it becomes very difficult to trust anything coming out of a promoter entity which has previously been accused of wrong BSE filings. IMHO avoiding permanent loss of capital is and should always be the first course of action when deciding where to invest one;\'s monies. We don’t need to hit a shot on every ball that is pitched to us. Due to serious risks WRT the promoter entity, IMV any time spend on business analysis would be time I could spend analyzing any other business, because anyway a meaningful allocation cannot be made to a microcap where promoter entities have open ED and CBI cases directly related to stock manipulation. With serious cases like these, it anyways becomes very difficult for an investor to expect any serious rerating of the underlying business. That takes away 1 engine of strong stock price appreciation among the 2 (earnings expansion and valuation expansion).\nThe only thing which would make me change my mind is complete recusal by High Court or Supreme Court. Even if that were to happen, it would take years. Hence, I will be giving this company a skip.','May 10, 2021 3:35 am'),(96,279,1,'Yes, I was worried about this. Even though the firm itself seems to be dealing quite decently, That was a big negative.\nI encountered the mining related reports, but not the incorrect filing one. Given the above I totally agree with you. If I cannot trust the filed reports then everything else is just thin air.\nDisclosure: Exited completely as the risks are disproportionate.','May 10, 2021 11:16 am'),(97,279,3,'Thank you for the analysis.\nThe company seemed interesting. Specially their flexible packaging business.\nWhile doing some quick due diligence, I noticed that the two largest public shareholders are ‘Amarjyoti Vanijya LLP’ and ‘Makrana Tradecom LLP’. Further googled these names and found out the following details:\nPartners in the Amarjyoti LLP are Ved Prakash Agarwal, Vikram Agarwal and others.\nPartners for Makrana Tradecom LLp are not mentioned\nEmail ids, and registered addresses for the companies are the exact same.\nHow should we interpret this? Is this a red flag? Why would promoter own a stake in the company through a LLP?\nSource:\nAMARJOTI VANIJYA LLP - Company, directors and contact details | Zauba Corp\nMAKRANA TRADECOM PRIVATE LIMITED - Company, directors and contact details | Zauba Corp','May 10, 2021 8:42 pm'),(98,279,1,'Well, to be honest, this is beyond my circle of competence. Additionally, I have exited based on the findings shared above regarding the open cases against promoters.\nBut my initial reaction here is ‘I don’t like it’. There could be many reasons from taxation or other purposes, but no matter what, it indicates that the promoters are doing more than minding their business, which is what I would expect an earnest promoter to be doing.\nSomeone with experience in these matters though, would be better placed to provide a more objective response.','May 10, 2021 8:59 pm');
/*!40000 ALTER TABLE `topicdiscussion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `UserId` int NOT NULL AUTO_INCREMENT,
  `UserName` varchar(100) DEFAULT NULL,
  `UserCreatedDate` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`UserId`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'blue','2021-05-10 20:08:19'),(2,'sahil_vi','2021-05-10 22:43:33'),(3,'Gaurav_Patil','2021-05-10 22:46:04');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'valuepickrdb'
--

--
-- Dumping routines for database 'valuepickrdb'
--
/*!50003 DROP PROCEDURE IF EXISTS `getTopic` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`admin`@`%` PROCEDURE `getTopic`()
BEGIN
select TopicId,TopicName,TopicURL from topic;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `getUserDetails` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`admin`@`%` PROCEDURE `getUserDetails`(In usernameIn varchar(100) )
BEGIN
select userId from user where UserName=usernameIn;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `SP_Insert_topic` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`admin`@`%` PROCEDURE `SP_Insert_topic`(IN topicnameIn varchar(200),In topicurls varchar(200))
BEGIN

    DECLARE CheckExists int;
    SET CheckExists = (SELECT count(*) from topic WHERE TopicURL = topicurls);
    select CheckExists;
    IF (CheckExists > 0) THEN
		select 'already exist';
    ELSE
        INSERT INTO `topic` (`TopicName`, `TopicURL`) values (topicnameIn,topicurls);
    END IF;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `SP_Insert_topicCategory` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`admin`@`%` PROCEDURE `SP_Insert_topicCategory`(In topicidIn int,categorynameIn varchar(200))
BEGIN
 DECLARE CheckExists int;
    SET CheckExists = (SELECT count(*) from topiccategory WHERE TopicId = topicidIn and CategoryName=categorynameIn);
    IF (CheckExists > 0) THEN
		select CheckExists;
    ELSE
        INSERT INTO `topiccategory` (`TopicId`, `CategoryName`) values (topicidIn,categorynameIn);
    END IF;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `SP_Insert_TopicDiscussion` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`admin`@`%` PROCEDURE `SP_Insert_TopicDiscussion`(In topicidIn int, In useridIn int,discussiontextIn text,discussiondateIn varchar(100))
BEGIN
    DECLARE CheckExists int;
    SET CheckExists = (SELECT count(*) from topicdiscussion WHERE UserId=useridIn and DiscussionDate = discussiondateIn);
    IF (CheckExists > 0) THEN
		select CheckExists;
    ELSE
        INSERT INTO `topicdiscussion` (`TopicId`,`UserId`,`DiscussionText`,`DiscussionDate`) values (topicidIn,useridIn,discussiontextIn,discussiondateIn);
    END IF;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `SP_Insert_User` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`admin`@`%` PROCEDURE `SP_Insert_User`(In usernameIn Varchar(50))
BEGIN
	DECLARE CheckExists int;
    SET CheckExists = (SELECT count(*) from user WHERE UserName = usernameIn);
	IF (CheckExists > 0) THEN
        select CheckExists;
    ELSE
        INSERT INTO `user` (`username`) values (usernameIn);
    END IF;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-05-11 17:21:17
