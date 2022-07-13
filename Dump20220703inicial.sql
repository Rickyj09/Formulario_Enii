-- MySQL dump 10.13  Distrib 8.0.29, for Win64 (x86_64)
--
-- Host: localhost    Database: test_1
-- ------------------------------------------------------
-- Server version	8.0.29

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
-- Table structure for table `articulos`
--

DROP TABLE IF EXISTS `articulos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `articulos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `precio` float DEFAULT NULL,
  `iva` int DEFAULT NULL,
  `descripcion` varchar(255) DEFAULT NULL,
  `image` varchar(255) DEFAULT NULL,
  `stock` int DEFAULT NULL,
  `CategoriaId` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `CategoriaId` (`CategoriaId`),
  CONSTRAINT `articulos_ibfk_1` FOREIGN KEY (`CategoriaId`) REFERENCES `categorias` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `articulos`
--

LOCK TABLES `articulos` WRITE;
/*!40000 ALTER TABLE `articulos` DISABLE KEYS */;
/*!40000 ALTER TABLE `articulos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cat_form`
--

DROP TABLE IF EXISTS `cat_form`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cat_form` (
  `id` int NOT NULL AUTO_INCREMENT,
  `codigo` varchar(100) NOT NULL,
  `descr` varchar(200) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cat_form`
--

LOCK TABLES `cat_form` WRITE;
/*!40000 ALTER TABLE `cat_form` DISABLE KEYS */;
/*!40000 ALTER TABLE `cat_form` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `categorias`
--

DROP TABLE IF EXISTS `categorias`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categorias` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categorias`
--

LOCK TABLES `categorias` WRITE;
/*!40000 ALTER TABLE `categorias` DISABLE KEYS */;
/*!40000 ALTER TABLE `categorias` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `check_list`
--

DROP TABLE IF EXISTS `check_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `check_list` (
  `id_formulario` varchar(20) NOT NULL,
  `fecha_inspec_formulario` date NOT NULL,
  `valor` varchar(15) NOT NULL,
  `nombre_check_list` varchar(90) NOT NULL,
  `obs_check_list` varchar(90) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `check_list`
--

LOCK TABLES `check_list` WRITE;
/*!40000 ALTER TABLE `check_list` DISABLE KEYS */;
/*!40000 ALTER TABLE `check_list` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cliente`
--

DROP TABLE IF EXISTS `cliente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cliente` (
  `id_Cliente` int NOT NULL AUTO_INCREMENT,
  `nom_Cliente` varchar(45) NOT NULL,
  `iden_Cliente` varchar(15) NOT NULL,
  `dir_Cliente` varchar(95) NOT NULL,
  `ciu_Cliente` varchar(45) NOT NULL,
  `contacto_Cliente` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id_Cliente`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='tabla en base al archivo enviado';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cliente`
--

LOCK TABLES `cliente` WRITE;
/*!40000 ALTER TABLE `cliente` DISABLE KEYS */;
/*!40000 ALTER TABLE `cliente` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cod_rep`
--

DROP TABLE IF EXISTS `cod_rep`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cod_rep` (
  `id` int NOT NULL AUTO_INCREMENT,
  `prefijo` varchar(45) DEFAULT NULL,
  `sec` decimal(25,0) DEFAULT NULL,
  `id_for` int DEFAULT NULL,
  `nombre` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='códiigo de cada reporte';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cod_rep`
--

LOCK TABLES `cod_rep` WRITE;
/*!40000 ALTER TABLE `cod_rep` DISABLE KEYS */;
/*!40000 ALTER TABLE `cod_rep` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `codigo`
--

DROP TABLE IF EXISTS `codigo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `codigo` (
  `id` int NOT NULL AUTO_INCREMENT,
  `preffijo` varchar(115) NOT NULL,
  `sec` decimal(25,0) DEFAULT NULL,
  `id_for` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_cod_idx` (`id_for`),
  CONSTRAINT `fk_catf` FOREIGN KEY (`id_for`) REFERENCES `cat_form` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `codigo`
--

LOCK TABLES `codigo` WRITE;
/*!40000 ALTER TABLE `codigo` DISABLE KEYS */;
/*!40000 ALTER TABLE `codigo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `condicion`
--

DROP TABLE IF EXISTS `condicion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `condicion` (
  `id_condicion` varchar(10) NOT NULL,
  `des_condicion` varchar(45) NOT NULL,
  PRIMARY KEY (`id_condicion`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `condicion`
--

LOCK TABLES `condicion` WRITE;
/*!40000 ALTER TABLE `condicion` DISABLE KEYS */;
/*!40000 ALTER TABLE `condicion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `datos_bloques_carga`
--

DROP TABLE IF EXISTS `datos_bloques_carga`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `datos_bloques_carga` (
  `idDATOS_BLOQUES_CARGA` int NOT NULL AUTO_INCREMENT,
  `CAPACIDAD_BLOQUE_PRIN_DATOS_BLOQUES_CARGA` varchar(45) NOT NULL,
  `CAPACIDAD_BLOQUE_AUX_DATOS_BLOQUES_CARGA` varchar(45) NOT NULL,
  `DIÁMETRO_CABLE_DATOS_BLOQUES_CARGA` varchar(45) NOT NULL,
  PRIMARY KEY (`idDATOS_BLOQUES_CARGA`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `datos_bloques_carga`
--

LOCK TABLES `datos_bloques_carga` WRITE;
/*!40000 ALTER TABLE `datos_bloques_carga` DISABLE KEYS */;
/*!40000 ALTER TABLE `datos_bloques_carga` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `datos_equipo`
--

DROP TABLE IF EXISTS `datos_equipo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `datos_equipo` (
  `id_datos_equipo` int NOT NULL AUTO_INCREMENT,
  `MARCA_datos_equipo` varchar(100) NOT NULL,
  `serie_datos_equipo` varchar(100) NOT NULL,
  `tipo_datos_equipo` varchar(100) NOT NULL,
  `modelo_datos_equipo` varchar(100) NOT NULL,
  `cap_datos_equipo` varchar(100) NOT NULL,
  `km_datos_equipo` varchar(100) NOT NULL,
  `anio_datos_equipo` varchar(100) NOT NULL,
  `codint_datos_equipo` varchar(100) NOT NULL,
  `id_formulario` varchar(100) NOT NULL,
  `fec_formulario` datetime DEFAULT NULL,
  PRIMARY KEY (`id_datos_equipo`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `datos_equipo`
--

LOCK TABLES `datos_equipo` WRITE;
/*!40000 ALTER TABLE `datos_equipo` DISABLE KEYS */;
/*!40000 ALTER TABLE `datos_equipo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `datos_lmi`
--

DROP TABLE IF EXISTS `datos_lmi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `datos_lmi` (
  `id_DATOS_LMI` int NOT NULL AUTO_INCREMENT,
  `FABRICANTE_DATOS_LMI` varchar(45) NOT NULL,
  `MARCA_DATOS_LMI` varchar(45) NOT NULL,
  `MODELO_DATOS_LMI` varchar(45) NOT NULL,
  `SERIE_DATOS_LMI` varchar(45) NOT NULL,
  `id_formulario` varchar(20) NOT NULL,
  `fec_formulario` date NOT NULL,
  PRIMARY KEY (`id_DATOS_LMI`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `datos_lmi`
--

LOCK TABLES `datos_lmi` WRITE;
/*!40000 ALTER TABLE `datos_lmi` DISABLE KEYS */;
/*!40000 ALTER TABLE `datos_lmi` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `datos_motor`
--

DROP TABLE IF EXISTS `datos_motor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `datos_motor` (
  `idDatos_Motor` int NOT NULL AUTO_INCREMENT,
  `MARCA_Datos_Motor` varchar(45) NOT NULL,
  `SERIE_Datos_Motor` varchar(45) NOT NULL,
  `MODELO_Datos_Motor` varchar(45) NOT NULL,
  `HOROMETRO_Datos_Motor` varchar(45) NOT NULL,
  `id_formulario` varchar(20) NOT NULL,
  `fec_formulario` date NOT NULL,
  PRIMARY KEY (`idDatos_Motor`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `datos_motor`
--

LOCK TABLES `datos_motor` WRITE;
/*!40000 ALTER TABLE `datos_motor` DISABLE KEYS */;
/*!40000 ALTER TABLE `datos_motor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `empresa`
--

DROP TABLE IF EXISTS `empresa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `empresa` (
  `idEmpresa` int NOT NULL AUTO_INCREMENT,
  `Nombre_Empresa` varchar(50) NOT NULL,
  `Direccion_Empresa` varchar(100) NOT NULL,
  `Telefono_Empresa` varchar(12) DEFAULT NULL,
  `Email_Empresa` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`idEmpresa`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `empresa`
--

LOCK TABLES `empresa` WRITE;
/*!40000 ALTER TABLE `empresa` DISABLE KEYS */;
/*!40000 ALTER TABLE `empresa` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `equipos_ins`
--

DROP TABLE IF EXISTS `equipos_ins`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `equipos_ins` (
  `codigo` varchar(45) NOT NULL,
  `nombre` varchar(45) NOT NULL,
  `fecha_calib` date NOT NULL,
  `nombre_insp` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`codigo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='contiene los equipos con los que se realiza la inspeccion';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `equipos_ins`
--

LOCK TABLES `equipos_ins` WRITE;
/*!40000 ALTER TABLE `equipos_ins` DISABLE KEYS */;
/*!40000 ALTER TABLE `equipos_ins` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `formulario`
--

DROP TABLE IF EXISTS `formulario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `formulario` (
  `id_formulario` int NOT NULL AUTO_INCREMENT,
  `llave_formulario` varchar(45) NOT NULL,
  `num_rep` varchar(45) DEFAULT NULL,
  `desc_formulario` varchar(65) DEFAULT NULL,
  `fecha_inspec_formulario` date NOT NULL,
  `fecha_emision_formulario` date NOT NULL,
  `fecha_expiracion_formulario` date NOT NULL,
  `lugar_ins_formulario` varchar(90) NOT NULL,
  `nom_inspe_formulario` varchar(95) DEFAULT NULL,
  `empresa` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id_formulario`)
) ENGINE=InnoDB AUTO_INCREMENT=137 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `formulario`
--

LOCK TABLES `formulario` WRITE;
/*!40000 ALTER TABLE `formulario` DISABLE KEYS */;
/*!40000 ALTER TABLE `formulario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `frapa`
--

DROP TABLE IF EXISTS `frapa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `frapa` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_formulario` int NOT NULL,
  `fec_formulario` date NOT NULL,
  `proc` varchar(45) DEFAULT NULL,
  `revis` varchar(45) DEFAULT NULL,
  `nivel_il` varchar(45) DEFAULT NULL,
  `con_sup` varchar(45) DEFAULT NULL,
  `met_insp` varchar(45) DEFAULT NULL,
  `tipo_il` varchar(45) DEFAULT NULL,
  `check1` varchar(45) DEFAULT NULL,
  `check2` varchar(45) DEFAULT NULL,
  `check3` varchar(45) DEFAULT NULL,
  `detalle` varchar(45) DEFAULT NULL,
  `proc_p` varchar(45) DEFAULT NULL,
  `revis_p` varchar(45) DEFAULT NULL,
  `temp_ens` varchar(45) DEFAULT NULL,
  `tipo_il_p` varchar(45) DEFAULT NULL,
  `nivel_il_p` varchar(45) DEFAULT NULL,
  `mater_base` varchar(45) DEFAULT NULL,
  `tipo_sec` varchar(45) DEFAULT NULL,
  `tipo_pen` varchar(45) DEFAULT NULL,
  `marca_kit` varchar(45) DEFAULT NULL,
  `tiem_pen` varchar(45) DEFAULT NULL,
  `met_rem` varchar(45) DEFAULT NULL,
  `marca_kit1` varchar(45) DEFAULT NULL,
  `tiem_sec` varchar(45) DEFAULT NULL,
  `for_rev` varchar(45) DEFAULT NULL,
  `marca_kit2` varchar(45) DEFAULT NULL,
  `tiem_rev` varchar(45) DEFAULT NULL,
  `equipo` varchar(45) DEFAULT NULL,
  `modelo` varchar(45) DEFAULT NULL,
  `iden` varchar(45) DEFAULT NULL,
  `c1` varchar(45) DEFAULT NULL,
  `c2` varchar(45) DEFAULT NULL,
  `c3` varchar(45) DEFAULT NULL,
  `c4` varchar(45) DEFAULT NULL,
  `c5` varchar(45) DEFAULT NULL,
  `c6` varchar(45) DEFAULT NULL,
  `c7` varchar(45) DEFAULT NULL,
  `c8` varchar(45) DEFAULT NULL,
  `c9` varchar(45) DEFAULT NULL,
  `c10` varchar(45) DEFAULT NULL,
  `c11` varchar(45) DEFAULT NULL,
  `c12` varchar(45) DEFAULT NULL,
  `c13` varchar(45) DEFAULT NULL,
  `c14` varchar(45) DEFAULT NULL,
  `c15` varchar(45) DEFAULT NULL,
  `c16` varchar(45) DEFAULT NULL,
  `c17` varchar(45) DEFAULT NULL,
  `c18` varchar(45) DEFAULT NULL,
  `c19` varchar(45) DEFAULT NULL,
  `c20` varchar(45) DEFAULT NULL,
  `c21` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `frapa`
--

LOCK TABLES `frapa` WRITE;
/*!40000 ALTER TABLE `frapa` DISABLE KEYS */;
/*!40000 ALTER TABLE `frapa` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `frapa1`
--

DROP TABLE IF EXISTS `frapa1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `frapa1` (
  `num` int NOT NULL AUTO_INCREMENT,
  `tipo_acc` varchar(45) DEFAULT NULL,
  `ref` varchar(45) DEFAULT NULL,
  `cod_enii` varchar(45) DEFAULT NULL,
  `medidas` varchar(45) DEFAULT NULL,
  `capac` varchar(45) DEFAULT NULL,
  `medida_cu` varchar(45) DEFAULT NULL,
  `vt` varchar(45) DEFAULT NULL,
  `pt` varchar(45) DEFAULT NULL,
  `id_f12` int NOT NULL,
  PRIMARY KEY (`num`),
  KEY `fk_f12_idx` (`id_f12`),
  CONSTRAINT `fk_frpol_f12` FOREIGN KEY (`id_f12`) REFERENCES `frapa` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `frapa1`
--

LOCK TABLES `frapa1` WRITE;
/*!40000 ALTER TABLE `frapa1` DISABLE KEYS */;
/*!40000 ALTER TABLE `frapa1` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `frcad`
--

DROP TABLE IF EXISTS `frcad`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `frcad` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_formulario` int NOT NULL,
  `fec_formulario` date NOT NULL,
  `proc` varchar(45) DEFAULT NULL,
  `revis` varchar(45) DEFAULT NULL,
  `nivel_il` varchar(45) DEFAULT NULL,
  `con_sup` varchar(45) DEFAULT NULL,
  `met_insp` varchar(45) DEFAULT NULL,
  `tipo_il` varchar(45) DEFAULT NULL,
  `check1` varchar(45) DEFAULT NULL,
  `check2` varchar(45) DEFAULT NULL,
  `check3` varchar(45) DEFAULT NULL,
  `detalle` varchar(45) DEFAULT NULL,
  `proc_p` varchar(45) DEFAULT NULL,
  `revis_p` varchar(45) DEFAULT NULL,
  `temp_ens` varchar(45) DEFAULT NULL,
  `tipo_il_p` varchar(45) DEFAULT NULL,
  `nivel_il_p` varchar(45) DEFAULT NULL,
  `mater_base` varchar(45) DEFAULT NULL,
  `tipo_sec` varchar(45) DEFAULT NULL,
  `tipo_pen` varchar(45) DEFAULT NULL,
  `marca_kit` varchar(45) DEFAULT NULL,
  `tiem_pen` varchar(45) DEFAULT NULL,
  `met_rem` varchar(45) DEFAULT NULL,
  `marca_kit1` varchar(45) DEFAULT NULL,
  `tiem_sec` varchar(45) DEFAULT NULL,
  `for_rev` varchar(45) DEFAULT NULL,
  `marca_kit2` varchar(45) DEFAULT NULL,
  `tiem_rev` varchar(45) DEFAULT NULL,
  `equipo` varchar(45) DEFAULT NULL,
  `modelo` varchar(45) DEFAULT NULL,
  `iden` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `frcad`
--

LOCK TABLES `frcad` WRITE;
/*!40000 ALTER TABLE `frcad` DISABLE KEYS */;
/*!40000 ALTER TABLE `frcad` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `frcad1`
--

DROP TABLE IF EXISTS `frcad1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `frcad1` (
  `num` int NOT NULL AUTO_INCREMENT,
  `tipo_ace` varchar(100) NOT NULL,
  `ref` varchar(45) DEFAULT NULL,
  `cod_enii` varchar(45) DEFAULT NULL,
  `eslabon` varchar(45) DEFAULT NULL,
  `medidas` varchar(45) DEFAULT NULL,
  `capac` varchar(45) DEFAULT NULL,
  `gancho1` varchar(45) DEFAULT NULL,
  `gancho2` varchar(45) DEFAULT NULL,
  `vt` varchar(45) DEFAULT NULL,
  `pt` varchar(45) DEFAULT NULL,
  `id_f4` int DEFAULT NULL,
  PRIMARY KEY (`num`),
  KEY `fk_f4_idx` (`id_f4`),
  CONSTRAINT `fk_f4` FOREIGN KEY (`id_f4`) REFERENCES `frcad` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `frcad1`
--

LOCK TABLES `frcad1` WRITE;
/*!40000 ALTER TABLE `frcad1` DISABLE KEYS */;
/*!40000 ALTER TABLE `frcad1` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `freca`
--

DROP TABLE IF EXISTS `freca`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `freca` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_formulario` int NOT NULL,
  `fec_formulario` date NOT NULL,
  `proc` varchar(45) DEFAULT NULL,
  `revis` varchar(45) DEFAULT NULL,
  `nivel_il` varchar(45) DEFAULT NULL,
  `con_sup` varchar(45) DEFAULT NULL,
  `met_insp` varchar(45) DEFAULT NULL,
  `tipo_il` varchar(45) DEFAULT NULL,
  `check1` varchar(45) DEFAULT NULL,
  `check2` varchar(45) DEFAULT NULL,
  `check3` varchar(45) DEFAULT NULL,
  `detalle` varchar(45) DEFAULT NULL,
  `elem_ens` varchar(45) DEFAULT NULL,
  `proc_p` varchar(45) DEFAULT NULL,
  `revis_p` varchar(45) DEFAULT NULL,
  `temp_ens` varchar(45) DEFAULT NULL,
  `tipo_il_p` varchar(45) DEFAULT NULL,
  `nivel_il_p` varchar(45) DEFAULT NULL,
  `mater_base` varchar(45) DEFAULT NULL,
  `tipo_sec` varchar(45) DEFAULT NULL,
  `tipo_pen` varchar(45) DEFAULT NULL,
  `marca_kit` varchar(45) DEFAULT NULL,
  `tiem_pen` varchar(45) DEFAULT NULL,
  `met_rem` varchar(45) DEFAULT NULL,
  `marca_kit1` varchar(45) DEFAULT NULL,
  `tiem_sec` varchar(45) DEFAULT NULL,
  `for_rev` varchar(45) DEFAULT NULL,
  `marca_kit2` varchar(45) DEFAULT NULL,
  `tiem_rev` varchar(45) DEFAULT NULL,
  `equipo` varchar(45) DEFAULT NULL,
  `modelo` varchar(45) DEFAULT NULL,
  `iden` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `freca`
--

LOCK TABLES `freca` WRITE;
/*!40000 ALTER TABLE `freca` DISABLE KEYS */;
/*!40000 ALTER TABLE `freca` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `freca1`
--

DROP TABLE IF EXISTS `freca1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `freca1` (
  `num` int NOT NULL AUTO_INCREMENT,
  `ref` varchar(45) DEFAULT NULL,
  `cod_enii` varchar(45) DEFAULT NULL,
  `tipo_ter` varchar(45) DEFAULT NULL,
  `medidas` varchar(45) DEFAULT NULL,
  `capac` varchar(45) DEFAULT NULL,
  `dia_elin` varchar(45) DEFAULT NULL,
  `med_aces` varchar(45) DEFAULT NULL,
  `vt` varchar(45) DEFAULT NULL,
  `pt` varchar(45) DEFAULT NULL,
  `id_f3` int DEFAULT NULL,
  PRIMARY KEY (`num`),
  KEY `id_f3_idx` (`id_f3`),
  CONSTRAINT `id_f3` FOREIGN KEY (`id_f3`) REFERENCES `freca` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `freca1`
--

LOCK TABLES `freca1` WRITE;
/*!40000 ALTER TABLE `freca1` DISABLE KEYS */;
/*!40000 ALTER TABLE `freca1` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `frefs`
--

DROP TABLE IF EXISTS `frefs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `frefs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_formulario` int NOT NULL,
  `fec_formulario` date NOT NULL,
  `proc` varchar(45) DEFAULT NULL,
  `revis` varchar(45) DEFAULT NULL,
  `nivel_il` varchar(45) DEFAULT NULL,
  `con_sup` varchar(45) DEFAULT NULL,
  `met_insp` varchar(45) DEFAULT NULL,
  `tipo_il` varchar(45) DEFAULT NULL,
  `check1` varchar(45) DEFAULT NULL,
  `check2` varchar(45) DEFAULT NULL,
  `check3` varchar(45) DEFAULT NULL,
  `detalle` varchar(45) DEFAULT NULL,
  `equipo` varchar(45) DEFAULT NULL,
  `modelo` varchar(45) DEFAULT NULL,
  `iden` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `frefs`
--

LOCK TABLES `frefs` WRITE;
/*!40000 ALTER TABLE `frefs` DISABLE KEYS */;
/*!40000 ALTER TABLE `frefs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `frefs1`
--

DROP TABLE IF EXISTS `frefs1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `frefs1` (
  `num` int NOT NULL AUTO_INCREMENT,
  `ref` varchar(45) DEFAULT NULL,
  `cod_enii` varchar(45) DEFAULT NULL,
  `tipo` varchar(45) DEFAULT NULL,
  `medidas` varchar(45) DEFAULT NULL,
  `capac` varchar(45) DEFAULT NULL,
  `vt` varchar(45) DEFAULT NULL,
  `id_f5` int DEFAULT NULL,
  PRIMARY KEY (`num`),
  KEY `fk_f5_idx` (`id_f5`),
  CONSTRAINT `fk_f5` FOREIGN KEY (`id_f5`) REFERENCES `frefs` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `frefs1`
--

LOCK TABLES `frefs1` WRITE;
/*!40000 ALTER TABLE `frefs1` DISABLE KEYS */;
/*!40000 ALTER TABLE `frefs1` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `frgan`
--

DROP TABLE IF EXISTS `frgan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `frgan` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_formulario` int NOT NULL,
  `fec_formulario` date NOT NULL,
  `proc` varchar(45) DEFAULT NULL,
  `revis` varchar(45) DEFAULT NULL,
  `nivel_il` varchar(45) DEFAULT NULL,
  `con_sup` varchar(45) DEFAULT NULL,
  `met_insp` varchar(45) DEFAULT NULL,
  `tipo_il` varchar(45) DEFAULT NULL,
  `check1` varchar(45) DEFAULT NULL,
  `check2` varchar(45) DEFAULT NULL,
  `check3` varchar(45) DEFAULT NULL,
  `detalle` varchar(45) DEFAULT NULL,
  `elem_en` varchar(45) DEFAULT NULL,
  `proc_p` varchar(45) DEFAULT NULL,
  `revis_p` varchar(45) DEFAULT NULL,
  `temp_ens` varchar(45) DEFAULT NULL,
  `tipo_il_p` varchar(45) DEFAULT NULL,
  `nivel_il_p` varchar(45) DEFAULT NULL,
  `mater_base` varchar(45) DEFAULT NULL,
  `tipo_sec` varchar(45) DEFAULT NULL,
  `tipo_pen` varchar(45) DEFAULT NULL,
  `marca_kit` varchar(45) DEFAULT NULL,
  `tiem_pen` varchar(45) DEFAULT NULL,
  `met_rem` varchar(45) DEFAULT NULL,
  `marca_kit1` varchar(45) DEFAULT NULL,
  `tiem_sec` varchar(45) DEFAULT NULL,
  `for_rev` varchar(45) DEFAULT NULL,
  `marca_kit2` varchar(45) DEFAULT NULL,
  `tiem_rev` varchar(45) DEFAULT NULL,
  `equipo` varchar(45) DEFAULT NULL,
  `modelo` varchar(45) DEFAULT NULL,
  `iden` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `frgan`
--

LOCK TABLES `frgan` WRITE;
/*!40000 ALTER TABLE `frgan` DISABLE KEYS */;
/*!40000 ALTER TABLE `frgan` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `frgan1`
--

DROP TABLE IF EXISTS `frgan1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `frgan1` (
  `num` int NOT NULL AUTO_INCREMENT,
  `ref` varchar(45) DEFAULT NULL,
  `cod_enii` varchar(45) DEFAULT NULL,
  `asiento` varchar(45) DEFAULT NULL,
  `medidas` varchar(45) DEFAULT NULL,
  `capac` varchar(45) DEFAULT NULL,
  `garganta` varchar(45) DEFAULT NULL,
  `vt` varchar(45) DEFAULT NULL,
  `pt` varchar(45) DEFAULT NULL,
  `id_f6` int DEFAULT NULL,
  PRIMARY KEY (`num`),
  KEY `id_f6_idx` (`id_f6`),
  CONSTRAINT `id_f6` FOREIGN KEY (`id_f6`) REFERENCES `frgan` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `frgan1`
--

LOCK TABLES `frgan1` WRITE;
/*!40000 ALTER TABLE `frgan1` DISABLE KEYS */;
/*!40000 ALTER TABLE `frgan1` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `frgri`
--

DROP TABLE IF EXISTS `frgri`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `frgri` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_formulario` int NOT NULL,
  `fec_formulario` date NOT NULL,
  `proc` varchar(45) DEFAULT NULL,
  `revis` varchar(45) DEFAULT NULL,
  `nivel_il` varchar(45) DEFAULT NULL,
  `con_sup` varchar(45) DEFAULT NULL,
  `met_insp` varchar(45) DEFAULT NULL,
  `tipo_il` varchar(45) DEFAULT NULL,
  `check1` varchar(45) DEFAULT NULL,
  `check2` varchar(45) DEFAULT NULL,
  `check3` varchar(45) DEFAULT NULL,
  `detalle` varchar(45) DEFAULT NULL,
  `elem_en` varchar(45) DEFAULT NULL,
  `proc_p` varchar(45) DEFAULT NULL,
  `revis_p` varchar(45) DEFAULT NULL,
  `temp_ens` varchar(45) DEFAULT NULL,
  `tipo_il_p` varchar(45) DEFAULT NULL,
  `nivel_il_p` varchar(45) DEFAULT NULL,
  `mater_base` varchar(45) DEFAULT NULL,
  `tipo_sec` varchar(45) DEFAULT NULL,
  `tipo_pen` varchar(45) DEFAULT NULL,
  `marca_kit` varchar(45) DEFAULT NULL,
  `tiem_pen` varchar(45) DEFAULT NULL,
  `met_rem` varchar(45) DEFAULT NULL,
  `marca_kit1` varchar(45) DEFAULT NULL,
  `tiem_sec` varchar(45) DEFAULT NULL,
  `for_rev` varchar(45) DEFAULT NULL,
  `marca_kit2` varchar(45) DEFAULT NULL,
  `tiem_rev` varchar(45) DEFAULT NULL,
  `equipo` varchar(45) DEFAULT NULL,
  `modelo` varchar(45) DEFAULT NULL,
  `iden` varchar(45) DEFAULT NULL,
  `num` varchar(45) DEFAULT NULL,
  `ref` varchar(45) DEFAULT NULL,
  `cod_enii` varchar(45) DEFAULT NULL,
  `diam_cue` varchar(45) DEFAULT NULL,
  `capac` varchar(45) DEFAULT NULL,
  `medidas` varchar(45) DEFAULT NULL,
  `vt` varchar(45) DEFAULT NULL,
  `pt` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `frgri`
--

LOCK TABLES `frgri` WRITE;
/*!40000 ALTER TABLE `frgri` DISABLE KEYS */;
/*!40000 ALTER TABLE `frgri` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `frgri1`
--

DROP TABLE IF EXISTS `frgri1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `frgri1` (
  `num` int NOT NULL AUTO_INCREMENT,
  `ref` varchar(45) DEFAULT NULL,
  `cod_enii` varchar(45) DEFAULT NULL,
  `medidas` varchar(45) DEFAULT NULL,
  `capac` varchar(45) DEFAULT NULL,
  `diam_cue` varchar(45) DEFAULT NULL,
  `vt` varchar(45) DEFAULT NULL,
  `pt` varchar(45) DEFAULT NULL,
  `id_f7` int DEFAULT NULL,
  PRIMARY KEY (`num`),
  KEY `id_f7_idx` (`id_f7`),
  CONSTRAINT `id_f7` FOREIGN KEY (`id_f7`) REFERENCES `frgri` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `frgri1`
--

LOCK TABLES `frgri1` WRITE;
/*!40000 ALTER TABLE `frgri1` DISABLE KEYS */;
/*!40000 ALTER TABLE `frgri1` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `frhor`
--

DROP TABLE IF EXISTS `frhor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `frhor` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_formulario` int NOT NULL,
  `fec_formulario` date NOT NULL,
  `proc` varchar(45) DEFAULT NULL,
  `revis` varchar(45) DEFAULT NULL,
  `nivel_il` varchar(45) DEFAULT NULL,
  `con_sup` varchar(45) DEFAULT NULL,
  `met_insp` varchar(45) DEFAULT NULL,
  `tipo_il` varchar(45) DEFAULT NULL,
  `check1` varchar(45) DEFAULT NULL,
  `check2` varchar(45) DEFAULT NULL,
  `check3` varchar(45) DEFAULT NULL,
  `detalle` varchar(45) DEFAULT NULL,
  `proc_p` varchar(45) DEFAULT NULL,
  `revis_p` varchar(45) DEFAULT NULL,
  `temp_ens` varchar(45) DEFAULT NULL,
  `tipo_il_p` varchar(45) DEFAULT NULL,
  `nivel_il_p` varchar(45) DEFAULT NULL,
  `mater_base` varchar(45) DEFAULT NULL,
  `tipo_sec` varchar(45) DEFAULT NULL,
  `tipo_pen` varchar(45) DEFAULT NULL,
  `marca_kit` varchar(45) DEFAULT NULL,
  `tiem_pen` varchar(45) DEFAULT NULL,
  `met_rem` varchar(45) DEFAULT NULL,
  `marca_kit1` varchar(45) DEFAULT NULL,
  `tiem_sec` varchar(45) DEFAULT NULL,
  `for_rev` varchar(45) DEFAULT NULL,
  `marca_kit2` varchar(45) DEFAULT NULL,
  `tiem_rev` varchar(45) DEFAULT NULL,
  `equipo` varchar(45) DEFAULT NULL,
  `modelo` varchar(45) DEFAULT NULL,
  `iden` varchar(45) DEFAULT NULL,
  `marca_hd` varchar(45) DEFAULT NULL,
  `iden_hd` varchar(45) DEFAULT NULL,
  `modelo_hd` varchar(45) DEFAULT NULL,
  `capac_hd` varchar(45) DEFAULT NULL,
  `medidas_hd` varchar(45) DEFAULT NULL,
  `marca_hi` varchar(45) DEFAULT NULL,
  `iden_hi` varchar(45) DEFAULT NULL,
  `modelo_hi` varchar(45) DEFAULT NULL,
  `capac_hi` varchar(45) DEFAULT NULL,
  `medidas_hi` varchar(45) DEFAULT NULL,
  `marca_hd1` varchar(45) DEFAULT NULL,
  `iden_hd1` varchar(45) DEFAULT NULL,
  `marca_hi1` varchar(45) DEFAULT NULL,
  `iden_hi1` varchar(45) DEFAULT NULL,
  `med_asi_hd` varchar(45) DEFAULT NULL,
  `med_asi_hi` varchar(45) DEFAULT NULL,
  `obs` varchar(45) DEFAULT NULL,
  `vt` varchar(45) DEFAULT NULL,
  `pt` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `frhor`
--

LOCK TABLES `frhor` WRITE;
/*!40000 ALTER TABLE `frhor` DISABLE KEYS */;
/*!40000 ALTER TABLE `frhor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `frkpi`
--

DROP TABLE IF EXISTS `frkpi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `frkpi` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_formulario` int NOT NULL,
  `fec_formulario` date NOT NULL,
  `proc` varchar(45) DEFAULT NULL,
  `revis` varchar(45) DEFAULT NULL,
  `nivel_il` varchar(45) DEFAULT NULL,
  `con_sup` varchar(45) DEFAULT NULL,
  `met_insp` varchar(45) DEFAULT NULL,
  `tipo_il` varchar(45) DEFAULT NULL,
  `check1` varchar(45) DEFAULT NULL,
  `check2` varchar(45) DEFAULT NULL,
  `check3` varchar(45) DEFAULT NULL,
  `detalle` varchar(45) DEFAULT NULL,
  `elem_en` varchar(45) DEFAULT NULL,
  `proc_p` varchar(45) DEFAULT NULL,
  `revis_p` varchar(45) DEFAULT NULL,
  `temp_ens` varchar(45) DEFAULT NULL,
  `tipo_il_p` varchar(45) DEFAULT NULL,
  `nivel_il_p` varchar(45) DEFAULT NULL,
  `mater_base` varchar(45) DEFAULT NULL,
  `tipo_sec` varchar(45) DEFAULT NULL,
  `tipo_pen` varchar(45) DEFAULT NULL,
  `marca_kit` varchar(45) DEFAULT NULL,
  `tiem_pen` varchar(45) DEFAULT NULL,
  `met_rem` varchar(45) DEFAULT NULL,
  `marca_kit1` varchar(45) DEFAULT NULL,
  `tiem_sec` varchar(45) DEFAULT NULL,
  `for_rev` varchar(45) DEFAULT NULL,
  `marca_kit2` varchar(45) DEFAULT NULL,
  `tiem_rev` varchar(45) DEFAULT NULL,
  `equipo` varchar(45) DEFAULT NULL,
  `marca` varchar(45) DEFAULT NULL,
  `iden` varchar(45) DEFAULT NULL,
  `marca_pk` varchar(45) DEFAULT NULL,
  `iden_pk` varchar(45) DEFAULT NULL,
  `modelo_pk` varchar(45) DEFAULT NULL,
  `capac_pk` varchar(45) DEFAULT NULL,
  `dia_sup` varchar(45) DEFAULT NULL,
  `dia_cen` varchar(45) DEFAULT NULL,
  `dia_inf` varchar(45) DEFAULT NULL,
  `obs` varchar(45) DEFAULT NULL,
  `vt` varchar(45) DEFAULT NULL,
  `pt` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `frkpi`
--

LOCK TABLES `frkpi` WRITE;
/*!40000 ALTER TABLE `frkpi` DISABLE KEYS */;
/*!40000 ALTER TABLE `frkpi` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `frpol`
--

DROP TABLE IF EXISTS `frpol`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `frpol` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_formulario` int NOT NULL,
  `fec_formulario` date NOT NULL,
  `proc` varchar(45) DEFAULT NULL,
  `revis` varchar(45) DEFAULT NULL,
  `nivel_il` varchar(45) DEFAULT NULL,
  `con_sup` varchar(45) DEFAULT NULL,
  `met_insp` varchar(45) DEFAULT NULL,
  `tipo_il` varchar(45) DEFAULT NULL,
  `check1` varchar(45) DEFAULT NULL,
  `check2` varchar(45) DEFAULT NULL,
  `check3` varchar(45) DEFAULT NULL,
  `detalle` varchar(45) DEFAULT NULL,
  `proc_p` varchar(45) DEFAULT NULL,
  `revis_p` varchar(45) DEFAULT NULL,
  `temp_ens` varchar(45) DEFAULT NULL,
  `tipo_il_p` varchar(45) DEFAULT NULL,
  `nivel_il_p` varchar(45) DEFAULT NULL,
  `mater_base` varchar(45) DEFAULT NULL,
  `tipo_sec` varchar(45) DEFAULT NULL,
  `tipo_pen` varchar(45) DEFAULT NULL,
  `marca_kit` varchar(45) DEFAULT NULL,
  `tiem_pen` varchar(45) DEFAULT NULL,
  `met_rem` varchar(45) DEFAULT NULL,
  `marca_kit1` varchar(45) DEFAULT NULL,
  `tiem_sec` varchar(45) DEFAULT NULL,
  `for_rev` varchar(45) DEFAULT NULL,
  `marca_kit2` varchar(45) DEFAULT NULL,
  `tiem_rev` varchar(45) DEFAULT NULL,
  `equipo` varchar(45) DEFAULT NULL,
  `modelo` varchar(45) DEFAULT NULL,
  `iden` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `frpol`
--

LOCK TABLES `frpol` WRITE;
/*!40000 ALTER TABLE `frpol` DISABLE KEYS */;
/*!40000 ALTER TABLE `frpol` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `frpol1`
--

DROP TABLE IF EXISTS `frpol1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `frpol1` (
  `num` int NOT NULL AUTO_INCREMENT,
  `ref` varchar(45) DEFAULT NULL,
  `cod_enii` varchar(45) DEFAULT NULL,
  `ancho` varchar(45) DEFAULT NULL,
  `diam` varchar(45) DEFAULT NULL,
  `vt` varchar(45) DEFAULT NULL,
  `pt` varchar(45) DEFAULT NULL,
  `id_f2` int DEFAULT NULL,
  PRIMARY KEY (`num`),
  KEY `fk_f2_idx` (`id_f2`),
  CONSTRAINT `fk_f2` FOREIGN KEY (`id_f2`) REFERENCES `frpol` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `frpol1`
--

LOCK TABLES `frpol1` WRITE;
/*!40000 ALTER TABLE `frpol1` DISABLE KEYS */;
/*!40000 ALTER TABLE `frpol1` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `frppr`
--

DROP TABLE IF EXISTS `frppr`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `frppr` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_formulario` int NOT NULL,
  `fec_formulario` date NOT NULL,
  `proc` varchar(45) DEFAULT NULL,
  `revis` varchar(45) DEFAULT NULL,
  `nivel_il` varchar(45) DEFAULT NULL,
  `con_sup` varchar(45) DEFAULT NULL,
  `met_insp` varchar(45) DEFAULT NULL,
  `tipo_il` varchar(45) DEFAULT NULL,
  `check1` varchar(45) DEFAULT NULL,
  `check2` varchar(45) DEFAULT NULL,
  `check3` varchar(45) DEFAULT NULL,
  `detalle` varchar(45) DEFAULT NULL,
  `proc_p` varchar(45) DEFAULT NULL,
  `revis_p` varchar(45) DEFAULT NULL,
  `temp_ens` varchar(45) DEFAULT NULL,
  `tipo_il_p` varchar(45) DEFAULT NULL,
  `nivel_il_p` varchar(45) DEFAULT NULL,
  `mater_base` varchar(45) DEFAULT NULL,
  `tipo_sec` varchar(45) DEFAULT NULL,
  `tipo_pen` varchar(45) DEFAULT NULL,
  `marca_kit` varchar(45) DEFAULT NULL,
  `tiem_pen` varchar(45) DEFAULT NULL,
  `met_rem` varchar(45) DEFAULT NULL,
  `marca_kit1` varchar(45) DEFAULT NULL,
  `tiem_sec` varchar(45) DEFAULT NULL,
  `for_rev` varchar(45) DEFAULT NULL,
  `marca_kit2` varchar(45) DEFAULT NULL,
  `tiem_rev` varchar(45) DEFAULT NULL,
  `equipo` varchar(45) DEFAULT NULL,
  `modelo` varchar(45) DEFAULT NULL,
  `iden` varchar(45) DEFAULT NULL,
  `marca_pas` varchar(45) DEFAULT NULL,
  `iden_pas` varchar(45) DEFAULT NULL,
  `modelo_pas` varchar(45) DEFAULT NULL,
  `capac_pas` varchar(45) DEFAULT NULL,
  `numero` varchar(45) DEFAULT NULL,
  `marca` varchar(45) DEFAULT NULL,
  `iden1` varchar(45) DEFAULT NULL,
  `asi_gan` varchar(45) DEFAULT NULL,
  `gar_gan` varchar(45) DEFAULT NULL,
  `med_gri` varchar(45) DEFAULT NULL,
  `obs` varchar(45) DEFAULT NULL,
  `vt` varchar(45) DEFAULT NULL,
  `pt` varchar(45) DEFAULT NULL,
  `tipo_pa` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `frppr`
--

LOCK TABLES `frppr` WRITE;
/*!40000 ALTER TABLE `frppr` DISABLE KEYS */;
/*!40000 ALTER TABLE `frppr` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `frqru`
--

DROP TABLE IF EXISTS `frqru`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `frqru` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_formulario` int NOT NULL,
  `fec_formulario` date NOT NULL,
  `proc` varchar(45) DEFAULT NULL,
  `revis` varchar(45) DEFAULT NULL,
  `nivel_il` varchar(45) DEFAULT NULL,
  `con_sup` varchar(45) DEFAULT NULL,
  `met_insp` varchar(45) DEFAULT NULL,
  `tipo_il` varchar(45) DEFAULT NULL,
  `check1` varchar(45) DEFAULT NULL,
  `check2` varchar(45) DEFAULT NULL,
  `check3` varchar(45) DEFAULT NULL,
  `detalle` varchar(45) DEFAULT NULL,
  `proc_p` varchar(45) DEFAULT NULL,
  `revis_p` varchar(45) DEFAULT NULL,
  `temp_ens` varchar(45) DEFAULT NULL,
  `tipo_il_p` varchar(45) DEFAULT NULL,
  `nivel_il_p` varchar(45) DEFAULT NULL,
  `mater_base` varchar(45) DEFAULT NULL,
  `tipo_sec` varchar(45) DEFAULT NULL,
  `tipo_pen` varchar(45) DEFAULT NULL,
  `marca_kit` varchar(45) DEFAULT NULL,
  `tiem_pen` varchar(45) DEFAULT NULL,
  `met_rem` varchar(45) DEFAULT NULL,
  `marca_kit1` varchar(45) DEFAULT NULL,
  `tiem_sec` varchar(45) DEFAULT NULL,
  `for_rev` varchar(45) DEFAULT NULL,
  `marca_kit2` varchar(45) DEFAULT NULL,
  `tiem_rev` varchar(45) DEFAULT NULL,
  `equipo` varchar(45) DEFAULT NULL,
  `marca` varchar(45) DEFAULT NULL,
  `iden` varchar(45) DEFAULT NULL,
  `marca_pk` varchar(45) DEFAULT NULL,
  `iden_pk` varchar(45) DEFAULT NULL,
  `modelo_pk` varchar(45) DEFAULT NULL,
  `capac_pk` varchar(45) DEFAULT NULL,
  `obs` varchar(45) DEFAULT NULL,
  `vt` varchar(45) DEFAULT NULL,
  `pt` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `frqru`
--

LOCK TABLES `frqru` WRITE;
/*!40000 ALTER TABLE `frqru` DISABLE KEYS */;
/*!40000 ALTER TABLE `frqru` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `frsep`
--

DROP TABLE IF EXISTS `frsep`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `frsep` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_formulario` int NOT NULL,
  `fec_formulario` date NOT NULL,
  `proc` varchar(45) DEFAULT NULL,
  `revis` varchar(45) DEFAULT NULL,
  `nivel_il` varchar(45) DEFAULT NULL,
  `con_sup` varchar(45) DEFAULT NULL,
  `met_insp` varchar(45) DEFAULT NULL,
  `tipo_il` varchar(45) DEFAULT NULL,
  `check1` varchar(45) DEFAULT NULL,
  `check2` varchar(45) DEFAULT NULL,
  `check3` varchar(45) DEFAULT NULL,
  `detalle` varchar(45) DEFAULT NULL,
  `proc_p` varchar(45) DEFAULT NULL,
  `revis_p` varchar(45) DEFAULT NULL,
  `temp_ens` varchar(45) DEFAULT NULL,
  `tipo_il_p` varchar(45) DEFAULT NULL,
  `nivel_il_p` varchar(45) DEFAULT NULL,
  `mater_base` varchar(45) DEFAULT NULL,
  `tipo_sec` varchar(45) DEFAULT NULL,
  `tipo_pen` varchar(45) DEFAULT NULL,
  `marca_kit` varchar(45) DEFAULT NULL,
  `tiem_pen` varchar(45) DEFAULT NULL,
  `met_rem` varchar(45) DEFAULT NULL,
  `marca_kit1` varchar(45) DEFAULT NULL,
  `tiem_sec` varchar(45) DEFAULT NULL,
  `for_rev` varchar(45) DEFAULT NULL,
  `marca_kit2` varchar(45) DEFAULT NULL,
  `tiem_rev` varchar(45) DEFAULT NULL,
  `marca_pk` varchar(45) DEFAULT NULL,
  `iden_pk` varchar(45) DEFAULT NULL,
  `modelo_pk` varchar(45) DEFAULT NULL,
  `capac_pk` varchar(45) DEFAULT NULL,
  `obs` varchar(45) DEFAULT NULL,
  `vt` varchar(45) DEFAULT NULL,
  `pt` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `frsep`
--

LOCK TABLES `frsep` WRITE;
/*!40000 ALTER TABLE `frsep` DISABLE KEYS */;
/*!40000 ALTER TABLE `frsep` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `frttr`
--

DROP TABLE IF EXISTS `frttr`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `frttr` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_formulario` int NOT NULL,
  `fec_formulario` date NOT NULL,
  `proc` varchar(45) DEFAULT NULL,
  `revis` varchar(45) DEFAULT NULL,
  `nivel_il` varchar(45) DEFAULT NULL,
  `con_sup` varchar(45) DEFAULT NULL,
  `met_insp` varchar(45) DEFAULT NULL,
  `tipo_il` varchar(45) DEFAULT NULL,
  `check1` varchar(45) DEFAULT NULL,
  `check2` varchar(45) DEFAULT NULL,
  `check3` varchar(45) DEFAULT NULL,
  `detalle` varchar(45) DEFAULT NULL,
  `ele_ens` varchar(45) DEFAULT NULL,
  `proc_p` varchar(45) DEFAULT NULL,
  `revis_p` varchar(45) DEFAULT NULL,
  `temp_ens` varchar(45) DEFAULT NULL,
  `tipo_il_p` varchar(45) DEFAULT NULL,
  `nivel_il_p` varchar(45) DEFAULT NULL,
  `mater_base` varchar(45) DEFAULT NULL,
  `tipo_sec` varchar(45) DEFAULT NULL,
  `tipo_pen` varchar(45) DEFAULT NULL,
  `marca_kit` varchar(45) DEFAULT NULL,
  `tiem_pen` varchar(45) DEFAULT NULL,
  `met_rem` varchar(45) DEFAULT NULL,
  `marca_kit1` varchar(45) DEFAULT NULL,
  `tiem_sec` varchar(45) DEFAULT NULL,
  `for_rev` varchar(45) DEFAULT NULL,
  `marca_kit2` varchar(45) DEFAULT NULL,
  `tiem_rev` varchar(45) DEFAULT NULL,
  `equipo` varchar(45) DEFAULT NULL,
  `modelo` varchar(45) DEFAULT NULL,
  `iden` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `frttr`
--

LOCK TABLES `frttr` WRITE;
/*!40000 ALTER TABLE `frttr` DISABLE KEYS */;
/*!40000 ALTER TABLE `frttr` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `frttr1`
--

DROP TABLE IF EXISTS `frttr1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `frttr1` (
  `num` int NOT NULL AUTO_INCREMENT,
  `ref` varchar(45) DEFAULT NULL,
  `cod_enii` varchar(45) DEFAULT NULL,
  `medidas` varchar(45) DEFAULT NULL,
  `capac` varchar(45) DEFAULT NULL,
  `gancho1` varchar(45) DEFAULT NULL,
  `gancho2` varchar(45) DEFAULT NULL,
  `vt` varchar(45) DEFAULT NULL,
  `pt` varchar(45) DEFAULT NULL,
  `id_f13` int NOT NULL,
  PRIMARY KEY (`num`),
  KEY `fk_f13_idx` (`id_f13`),
  CONSTRAINT `fk_frttr_f13` FOREIGN KEY (`id_f13`) REFERENCES `frttr` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `frttr1`
--

LOCK TABLES `frttr1` WRITE;
/*!40000 ALTER TABLE `frttr1` DISABLE KEYS */;
/*!40000 ALTER TABLE `frttr1` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ime`
--

DROP TABLE IF EXISTS `ime`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ime` (
  `id_ime` int NOT NULL,
  `nombre_nom_ime` varchar(45) NOT NULL COMMENT 'debe bajar de la tabla nom_ime',
  `observacion_ime` varchar(145) NOT NULL,
  `referencia_ime` varchar(145) DEFAULT NULL,
  `condicion_ime` varchar(45) NOT NULL,
  `numero_reporte` varchar(45) NOT NULL,
  PRIMARY KEY (`id_ime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ime`
--

LOCK TABLES `ime` WRITE;
/*!40000 ALTER TABLE `ime` DISABLE KEYS */;
/*!40000 ALTER TABLE `ime` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ins_doc_equipo`
--

DROP TABLE IF EXISTS `ins_doc_equipo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ins_doc_equipo` (
  `id_ins_doc_equipo` int NOT NULL AUTO_INCREMENT,
  `nombre_ins_doc_equipo` varchar(45) NOT NULL,
  `observaciones_ins_doc_equipo` varchar(115) DEFAULT NULL,
  `referencia_ins_doc_equipo` varchar(145) DEFAULT NULL,
  `condi_ins_doc_equipo` varchar(15) NOT NULL,
  PRIMARY KEY (`id_ins_doc_equipo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ins_doc_equipo`
--

LOCK TABLES `ins_doc_equipo` WRITE;
/*!40000 ALTER TABLE `ins_doc_equipo` DISABLE KEYS */;
/*!40000 ALTER TABLE `ins_doc_equipo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lmi`
--

DROP TABLE IF EXISTS `lmi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `lmi` (
  `id_lmi` int NOT NULL AUTO_INCREMENT,
  `fabricante_lmi` varchar(45) NOT NULL,
  `marca_lmi` varchar(45) NOT NULL,
  `modelo_lmi` varchar(45) NOT NULL,
  `serie_lmi` varchar(45) NOT NULL,
  PRIMARY KEY (`id_lmi`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lmi`
--

LOCK TABLES `lmi` WRITE;
/*!40000 ALTER TABLE `lmi` DISABLE KEYS */;
/*!40000 ALTER TABLE `lmi` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `nom_ime`
--

DROP TABLE IF EXISTS `nom_ime`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `nom_ime` (
  `id_nom_ime` int NOT NULL,
  `nombre_nom_ime` varchar(145) NOT NULL,
  PRIMARY KEY (`id_nom_ime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nom_ime`
--

LOCK TABLES `nom_ime` WRITE;
/*!40000 ALTER TABLE `nom_ime` DISABLE KEYS */;
/*!40000 ALTER TABLE `nom_ime` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `nombre_ins_doc_equipo`
--

DROP TABLE IF EXISTS `nombre_ins_doc_equipo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `nombre_ins_doc_equipo` (
  `id_nombre_ins_doc_equipo` int NOT NULL,
  `nombre_ins_doc_equipo` varchar(145) NOT NULL,
  PRIMARY KEY (`id_nombre_ins_doc_equipo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nombre_ins_doc_equipo`
--

LOCK TABLES `nombre_ins_doc_equipo` WRITE;
/*!40000 ALTER TABLE `nombre_ins_doc_equipo` DISABLE KEYS */;
/*!40000 ALTER TABLE `nombre_ins_doc_equipo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pasteca_pri`
--

DROP TABLE IF EXISTS `pasteca_pri`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pasteca_pri` (
  `id_pasteca_pri` int NOT NULL AUTO_INCREMENT,
  `marca_pasteca_pri` varchar(45) NOT NULL,
  `capacidad_pasteca_pri` varchar(45) NOT NULL,
  `modelo_pasteca_pri` varchar(45) NOT NULL,
  `serie_ref_pasteca_pri` varchar(45) NOT NULL,
  `diacab_pasteca_pri` int NOT NULL,
  `id_formulario` varchar(20) NOT NULL,
  `fec_formulario` date NOT NULL,
  PRIMARY KEY (`id_pasteca_pri`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pasteca_pri`
--

LOCK TABLES `pasteca_pri` WRITE;
/*!40000 ALTER TABLE `pasteca_pri` DISABLE KEYS */;
/*!40000 ALTER TABLE `pasteca_pri` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pasteca_sec`
--

DROP TABLE IF EXISTS `pasteca_sec`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pasteca_sec` (
  `id_pasteca_sec` int NOT NULL AUTO_INCREMENT,
  `marca_pasteca_sec` varchar(45) NOT NULL,
  `capacidad_pasteca_sec` varchar(45) NOT NULL,
  `modelo_pasteca_sec` varchar(45) NOT NULL,
  `serie_ref_pasteca_sec` varchar(45) NOT NULL,
  `diacab_pasteca_sec` int NOT NULL,
  `id_formulario` varchar(20) NOT NULL,
  `fec_formulario` date NOT NULL,
  PRIMARY KEY (`id_pasteca_sec`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pasteca_sec`
--

LOCK TABLES `pasteca_sec` WRITE;
/*!40000 ALTER TABLE `pasteca_sec` DISABLE KEYS */;
/*!40000 ALTER TABLE `pasteca_sec` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `prue_carg_din`
--

DROP TABLE IF EXISTS `prue_carg_din`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `prue_carg_din` (
  `id_formulario` varchar(20) NOT NULL,
  `carga_utilizada` decimal(12,0) DEFAULT NULL,
  `peso_carga` decimal(12,0) DEFAULT NULL,
  `peso_aparejos` decimal(12,0) DEFAULT NULL,
  `medida` varchar(45) DEFAULT NULL,
  `peso_total` decimal(12,0) DEFAULT NULL,
  `long_pluma` decimal(12,0) DEFAULT NULL,
  `radio_ope` decimal(12,0) DEFAULT NULL,
  `ang_pluma` decimal(12,0) DEFAULT NULL,
  `cap_max` int DEFAULT NULL,
  `tornamesa` varchar(45) DEFAULT NULL,
  `sis_mov_fre` varchar(45) DEFAULT NULL,
  `est_estabilizado` varchar(45) DEFAULT NULL,
  `cond_estab_maq` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `prue_carg_din`
--

LOCK TABLES `prue_carg_din` WRITE;
/*!40000 ALTER TABLE `prue_carg_din` DISABLE KEYS */;
/*!40000 ALTER TABLE `prue_carg_din` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `prue_carg_est`
--

DROP TABLE IF EXISTS `prue_carg_est`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `prue_carg_est` (
  `id_prue_carg_est` int NOT NULL AUTO_INCREMENT,
  `id_formulario` varchar(45) NOT NULL,
  `carga_utilizada` decimal(12,0) NOT NULL,
  `peso_carga` decimal(12,0) NOT NULL,
  `peso_aparejos` decimal(12,0) NOT NULL,
  `peso_total` decimal(12,0) NOT NULL,
  `medida` varchar(45) NOT NULL,
  `long_pluma` decimal(12,0) DEFAULT NULL,
  `radio_ope` decimal(12,0) DEFAULT NULL,
  `ang_pluma` decimal(12,0) DEFAULT NULL,
  `cap_max` int DEFAULT NULL,
  `tiempo` int DEFAULT NULL,
  `carga` decimal(12,0) DEFAULT NULL,
  `estab_1` decimal(12,0) DEFAULT NULL,
  `estab_2` decimal(12,0) DEFAULT NULL,
  `estab_3` decimal(12,0) DEFAULT NULL,
  `estab_4` decimal(12,0) DEFAULT NULL,
  PRIMARY KEY (`id_prue_carg_est`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Tabla de las pruebas carga estatica';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `prue_carg_est`
--

LOCK TABLES `prue_carg_est` WRITE;
/*!40000 ALTER TABLE `prue_carg_est` DISABLE KEYS */;
/*!40000 ALTER TABLE `prue_carg_est` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rep_foto_frapa`
--

DROP TABLE IF EXISTS `rep_foto_frapa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rep_foto_frapa` (
  `id` int NOT NULL AUTO_INCREMENT,
  `foto` varchar(255) DEFAULT NULL,
  `id_f` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_frapa_idx` (`id_f`),
  CONSTRAINT `fk_frapa` FOREIGN KEY (`id_f`) REFERENCES `frapa` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rep_foto_frapa`
--

LOCK TABLES `rep_foto_frapa` WRITE;
/*!40000 ALTER TABLE `rep_foto_frapa` DISABLE KEYS */;
/*!40000 ALTER TABLE `rep_foto_frapa` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rep_foto_frcad`
--

DROP TABLE IF EXISTS `rep_foto_frcad`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rep_foto_frcad` (
  `id` int NOT NULL AUTO_INCREMENT,
  `foto` varchar(255) DEFAULT NULL,
  `id_f` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_frcad_idx` (`id_f`),
  CONSTRAINT `fk_frcad` FOREIGN KEY (`id_f`) REFERENCES `frcad` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rep_foto_frcad`
--

LOCK TABLES `rep_foto_frcad` WRITE;
/*!40000 ALTER TABLE `rep_foto_frcad` DISABLE KEYS */;
/*!40000 ALTER TABLE `rep_foto_frcad` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rep_foto_freca`
--

DROP TABLE IF EXISTS `rep_foto_freca`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rep_foto_freca` (
  `id` int NOT NULL AUTO_INCREMENT,
  `foto` varchar(255) DEFAULT NULL,
  `id_f` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_fr2_idx` (`id_f`),
  CONSTRAINT `fk_fr2` FOREIGN KEY (`id_f`) REFERENCES `freca` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rep_foto_freca`
--

LOCK TABLES `rep_foto_freca` WRITE;
/*!40000 ALTER TABLE `rep_foto_freca` DISABLE KEYS */;
/*!40000 ALTER TABLE `rep_foto_freca` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rep_foto_frefs`
--

DROP TABLE IF EXISTS `rep_foto_frefs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rep_foto_frefs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `foto` varchar(255) DEFAULT NULL,
  `id_f` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_frefs_idx` (`id_f`),
  CONSTRAINT `fk_frefs` FOREIGN KEY (`id_f`) REFERENCES `frefs` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rep_foto_frefs`
--

LOCK TABLES `rep_foto_frefs` WRITE;
/*!40000 ALTER TABLE `rep_foto_frefs` DISABLE KEYS */;
/*!40000 ALTER TABLE `rep_foto_frefs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rep_foto_frgan`
--

DROP TABLE IF EXISTS `rep_foto_frgan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rep_foto_frgan` (
  `id` int NOT NULL AUTO_INCREMENT,
  `foto` varchar(255) DEFAULT NULL,
  `id_f` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_frgan_idx` (`id_f`),
  CONSTRAINT `fk_frgan` FOREIGN KEY (`id_f`) REFERENCES `frgan` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rep_foto_frgan`
--

LOCK TABLES `rep_foto_frgan` WRITE;
/*!40000 ALTER TABLE `rep_foto_frgan` DISABLE KEYS */;
/*!40000 ALTER TABLE `rep_foto_frgan` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rep_foto_frgri`
--

DROP TABLE IF EXISTS `rep_foto_frgri`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rep_foto_frgri` (
  `id` int NOT NULL AUTO_INCREMENT,
  `foto` varchar(255) DEFAULT NULL,
  `id_f` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_frgri_idx` (`id_f`),
  CONSTRAINT `fk_frgri` FOREIGN KEY (`id_f`) REFERENCES `frgri` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rep_foto_frgri`
--

LOCK TABLES `rep_foto_frgri` WRITE;
/*!40000 ALTER TABLE `rep_foto_frgri` DISABLE KEYS */;
/*!40000 ALTER TABLE `rep_foto_frgri` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rep_foto_frhor`
--

DROP TABLE IF EXISTS `rep_foto_frhor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rep_foto_frhor` (
  `id` int NOT NULL AUTO_INCREMENT,
  `foto` varchar(255) DEFAULT NULL,
  `id_f` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_frhor_idx` (`id_f`),
  CONSTRAINT `fk_frhor` FOREIGN KEY (`id_f`) REFERENCES `frhor` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rep_foto_frhor`
--

LOCK TABLES `rep_foto_frhor` WRITE;
/*!40000 ALTER TABLE `rep_foto_frhor` DISABLE KEYS */;
/*!40000 ALTER TABLE `rep_foto_frhor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rep_foto_frkpi`
--

DROP TABLE IF EXISTS `rep_foto_frkpi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rep_foto_frkpi` (
  `id` int NOT NULL AUTO_INCREMENT,
  `foto` varchar(255) DEFAULT NULL,
  `id_f` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_frkpi_idx` (`id_f`),
  CONSTRAINT `fk_frkpi` FOREIGN KEY (`id_f`) REFERENCES `frkpi` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rep_foto_frkpi`
--

LOCK TABLES `rep_foto_frkpi` WRITE;
/*!40000 ALTER TABLE `rep_foto_frkpi` DISABLE KEYS */;
/*!40000 ALTER TABLE `rep_foto_frkpi` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rep_foto_frpol`
--

DROP TABLE IF EXISTS `rep_foto_frpol`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rep_foto_frpol` (
  `id` int NOT NULL AUTO_INCREMENT,
  `foto` varchar(255) DEFAULT NULL,
  `id_f` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rep_foto_frpol`
--

LOCK TABLES `rep_foto_frpol` WRITE;
/*!40000 ALTER TABLE `rep_foto_frpol` DISABLE KEYS */;
/*!40000 ALTER TABLE `rep_foto_frpol` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rep_foto_frppr`
--

DROP TABLE IF EXISTS `rep_foto_frppr`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rep_foto_frppr` (
  `id` int NOT NULL AUTO_INCREMENT,
  `foto` varchar(255) DEFAULT NULL,
  `id_f` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_frppr_idx` (`id_f`),
  CONSTRAINT `fk_frppr` FOREIGN KEY (`id_f`) REFERENCES `frppr` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rep_foto_frppr`
--

LOCK TABLES `rep_foto_frppr` WRITE;
/*!40000 ALTER TABLE `rep_foto_frppr` DISABLE KEYS */;
/*!40000 ALTER TABLE `rep_foto_frppr` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rep_foto_frqru`
--

DROP TABLE IF EXISTS `rep_foto_frqru`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rep_foto_frqru` (
  `id` int NOT NULL AUTO_INCREMENT,
  `foto` varchar(255) DEFAULT NULL,
  `id_f` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_frqru_idx` (`id_f`),
  CONSTRAINT `fk_frqru` FOREIGN KEY (`id_f`) REFERENCES `frqru` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rep_foto_frqru`
--

LOCK TABLES `rep_foto_frqru` WRITE;
/*!40000 ALTER TABLE `rep_foto_frqru` DISABLE KEYS */;
/*!40000 ALTER TABLE `rep_foto_frqru` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rep_foto_frsep`
--

DROP TABLE IF EXISTS `rep_foto_frsep`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rep_foto_frsep` (
  `id` int NOT NULL AUTO_INCREMENT,
  `foto` varchar(255) DEFAULT NULL,
  `id_f` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_frsep_idx` (`id_f`),
  CONSTRAINT `fk_frsep` FOREIGN KEY (`id_f`) REFERENCES `frsep` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rep_foto_frsep`
--

LOCK TABLES `rep_foto_frsep` WRITE;
/*!40000 ALTER TABLE `rep_foto_frsep` DISABLE KEYS */;
/*!40000 ALTER TABLE `rep_foto_frsep` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rep_foto_frttr`
--

DROP TABLE IF EXISTS `rep_foto_frttr`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rep_foto_frttr` (
  `id` int NOT NULL AUTO_INCREMENT,
  `foto` varchar(255) DEFAULT NULL,
  `id_f` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_frttr_idx` (`id_f`),
  CONSTRAINT `fk_frttr` FOREIGN KEY (`id_f`) REFERENCES `frttr` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rep_foto_frttr`
--

LOCK TABLES `rep_foto_frttr` WRITE;
/*!40000 ALTER TABLE `rep_foto_frttr` DISABLE KEYS */;
/*!40000 ALTER TABLE `rep_foto_frttr` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL,
  `password_hash` varchar(128) NOT NULL,
  `nombre` varchar(200) NOT NULL,
  `email` varchar(200) NOT NULL,
  `admin` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-07-03 19:50:11
