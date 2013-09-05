SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

DROP SCHEMA IF EXISTS `edfu` ;
CREATE SCHEMA IF NOT EXISTS `edfu` DEFAULT CHARACTER SET utf8 ;
USE `edfu` ;

-- -----------------------------------------------------
-- Table `edfu`.`tempel`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `edfu`.`tempel` ;

CREATE  TABLE IF NOT EXISTS `edfu`.`tempel` (
  `uid` INT NOT NULL ,
  `name` VARCHAR(255) NULL ,
  PRIMARY KEY (`uid`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `edfu`.`band`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `edfu`.`band` ;

CREATE  TABLE IF NOT EXISTS `edfu`.`band` (
  `uid` INT NOT NULL ,
  `nummer` INT NULL ,
  `freigegeben` TINYINT NULL ,
  `literatur` VARCHAR(255) NULL ,
  `tempel_uid` INT NOT NULL ,
  PRIMARY KEY (`uid`) ,
  INDEX `fk_band_tempel1_idx` (`tempel_uid` ASC) ,
  CONSTRAINT `fk_band_tempel1`
    FOREIGN KEY (`tempel_uid` )
    REFERENCES `edfu`.`tempel` (`uid` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `edfu`.`stelle`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `edfu`.`stelle` ;

CREATE  TABLE IF NOT EXISTS `edfu`.`stelle` (
  `uid` INT NOT NULL ,
  `band_uid` INT NOT NULL ,
  `seite_start` INT NULL ,
  `zeile_start` INT NULL ,
  `seite_stop` INT NULL ,
  `zeile_stop` INT NULL ,
  `anmerkung` TEXT NULL ,
  `stop_unsicher` TINYINT NULL ,
  `zerstoerung` TINYINT NULL ,
  INDEX `fk_belegstelle_band1_idx` (`band_uid` ASC) ,
  PRIMARY KEY (`uid`) ,
  CONSTRAINT `fk_belegstelle_band1`
    FOREIGN KEY (`band_uid` )
    REFERENCES `edfu`.`band` (`uid` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `edfu`.`formular`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `edfu`.`formular` ;

CREATE  TABLE IF NOT EXISTS `edfu`.`formular` (
  `uid` INT NOT NULL AUTO_INCREMENT ,
  `id` INT NOT NULL ,
  `stelle_uid` INT NOT NULL ,
  `transliteration` TEXT CHARACTER SET 'utf8' COLLATE 'utf8_unicode_ci' NOT NULL ,
  `uebersetzung` TEXT CHARACTER SET 'utf8' COLLATE 'utf8_unicode_ci' NULL ,
  `texttyp` TEXT CHARACTER SET 'utf8' COLLATE 'utf8_unicode_ci' NULL ,
  PRIMARY KEY (`uid`) ,
  INDEX `fk_FL_belegstelle1_idx` (`stelle_uid` ASC) ,
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) )
ENGINE = MyISAM
AUTO_INCREMENT = 10373
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_unicode_ci;


-- -----------------------------------------------------
-- Table `edfu`.`gott`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `edfu`.`gott` ;

CREATE  TABLE IF NOT EXISTS `edfu`.`gott` (
  `uid` INT NOT NULL AUTO_INCREMENT ,
  `id` INT NOT NULL ,
  `stelle_uid` INT NOT NULL ,
  `transliteration` TEXT CHARACTER SET 'utf8' NOT NULL ,
  `eponym` TEXT CHARACTER SET 'utf8' NULL ,
  `funktion` TEXT CHARACTER SET 'utf8' NULL ,
  `beziehung` TEXT CHARACTER SET 'utf8' NULL ,
  `ort` TEXT CHARACTER SET 'utf8' NULL ,
  `anmerkung` TEXT NULL ,
  PRIMARY KEY (`uid`) ,
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) ,
  INDEX `fk_gott_stelle1_idx` (`stelle_uid` ASC) )
ENGINE = MyISAM
AUTO_INCREMENT = 9471
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_unicode_ci;


-- -----------------------------------------------------
-- Table `edfu`.`ort`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `edfu`.`ort` ;

CREATE  TABLE IF NOT EXISTS `edfu`.`ort` (
  `uid` INT NOT NULL AUTO_INCREMENT ,
  `id` INT NOT NULL ,
  `transliteration` TEXT CHARACTER SET 'utf8' NOT NULL ,
  `ort` TEXT CHARACTER SET 'utf8' NULL ,
  `lokalisation` TEXT CHARACTER SET 'utf8' NULL ,
  `anmerkung` TEXT NULL ,
  PRIMARY KEY (`uid`) ,
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) )
ENGINE = MyISAM
AUTO_INCREMENT = 1250
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_unicode_ci;


-- -----------------------------------------------------
-- Table `edfu`.`wb_berlin`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `edfu`.`wb_berlin` ;

CREATE  TABLE IF NOT EXISTS `edfu`.`wb_berlin` (
  `uid` INT NOT NULL ,
  `band` INT NULL ,
  `seite_start` INT NULL ,
  `zeile_start` INT NULL ,
  `seite_stop` INT NULL ,
  `zeile_stop` INT NULL ,
  `vornach` INT NULL DEFAULT 0 ,
  `notiz` TEXT NULL ,
  `anmerkung` TEXT NULL ,
  PRIMARY KEY (`uid`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `edfu`.`wort`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `edfu`.`wort` ;

CREATE  TABLE IF NOT EXISTS `edfu`.`wort` (
  `uid` INT NOT NULL AUTO_INCREMENT ,
  `id` INT NOT NULL ,
  `transliteration` TEXT CHARACTER SET 'utf8' COLLATE 'utf8_unicode_ci' NOT NULL ,
  `uebersetzung` TEXT CHARACTER SET 'utf8' COLLATE 'utf8_unicode_ci' NULL ,
  `hieroglyph` VARCHAR(255) CHARACTER SET 'utf8' COLLATE 'utf8_unicode_ci' NULL ,
  `weiteres` TEXT NULL ,
  `anmerkung` TEXT NULL ,
  `lemma` VARCHAR(255) NULL ,
  `wb_berlin_uid` INT NULL ,
  PRIMARY KEY (`uid`) ,
  INDEX `fk_wort_berlin1_idx` (`wb_berlin_uid` ASC) ,
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) )
ENGINE = MyISAM
AUTO_INCREMENT = 4623
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_unicode_ci;


-- -----------------------------------------------------
-- Table `edfu`.`szene_bild`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `edfu`.`szene_bild` ;

CREATE  TABLE IF NOT EXISTS `edfu`.`szene_bild` (
  `uid` INT NOT NULL ,
  `name` VARCHAR(255) NULL ,
  `dateiname` VARCHAR(255) NULL ,
  `imagemap` VARCHAR(255) NULL ,
  `breite` INT NULL ,
  `hoehe` INT NULL ,
  `offset_x` INT NULL ,
  `offset_y` INT NULL ,
  `breite_original` INT NULL ,
  `hoehe_original` INT NULL ,
  PRIMARY KEY (`uid`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `edfu`.`szene`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `edfu`.`szene` ;

CREATE  TABLE IF NOT EXISTS `edfu`.`szene` (
  `uid` INT NOT NULL ,
  `nummer` INT NULL ,
  `beschreibung` TEXT NULL ,
  `szene_bild_uid` INT NULL ,
  `rect` VARCHAR(255) NULL ,
  `polygon` TEXT NULL ,
  `koordinate_x` DOUBLE NULL ,
  `koordinate_y` DOUBLE NULL ,
  `blickwinkel` INT NULL ,
  `breite` DOUBLE NULL ,
  `prozent_z` DOUBLE NULL ,
  `hoehe` DOUBLE NULL ,
  `grau` TINYINT NULL ,
  PRIMARY KEY (`uid`) ,
  INDEX `fk_szene_szene_bild1_idx` (`szene_bild_uid` ASC) ,
  CONSTRAINT `fk_szene_szene_bild1`
    FOREIGN KEY (`szene_bild_uid` )
    REFERENCES `edfu`.`szene_bild` (`uid` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `edfu`.`photo_typ`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `edfu`.`photo_typ` ;

CREATE  TABLE IF NOT EXISTS `edfu`.`photo_typ` (
  `uid` INT NOT NULL ,
  `name` VARCHAR(255) NULL ,
  `jahr` INT NULL ,
  PRIMARY KEY (`uid`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `edfu`.`photo`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `edfu`.`photo` ;

CREATE  TABLE IF NOT EXISTS `edfu`.`photo` (
  `uid` INT NOT NULL ,
  `photo_typ_uid` INT NOT NULL ,
  `name` VARCHAR(255) NULL ,
  PRIMARY KEY (`uid`) ,
  INDEX `fk_photo_photo_typ1_idx` (`photo_typ_uid` ASC) ,
  CONSTRAINT `fk_photo_photo_typ1`
    FOREIGN KEY (`photo_typ_uid` )
    REFERENCES `edfu`.`photo_typ` (`uid` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `edfu`.`literatur`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `edfu`.`literatur` ;

CREATE  TABLE IF NOT EXISTS `edfu`.`literatur` (
  `uid` INT NOT NULL ,
  `beschreibung` TEXT NULL ,
  PRIMARY KEY (`uid`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `edfu`.`formular_has_literatur`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `edfu`.`formular_has_literatur` ;

CREATE  TABLE IF NOT EXISTS `edfu`.`formular_has_literatur` (
  `uid_local` INT NOT NULL ,
  `uid_foreign` INT NOT NULL ,
  `detail` TEXT NULL ,
  PRIMARY KEY (`uid_local`, `uid_foreign`) ,
  INDEX `fk_FL_has_literatur_literatur1_idx` (`uid_foreign` ASC) ,
  INDEX `fk_FL_has_literatur_FL1_idx` (`uid_local` ASC) )
ENGINE = MyISAM
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_unicode_ci;


-- -----------------------------------------------------
-- Table `edfu`.`wort_has_stelle`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `edfu`.`wort_has_stelle` ;

CREATE  TABLE IF NOT EXISTS `edfu`.`wort_has_stelle` (
  `uid_local` INT NOT NULL ,
  `uid_foreign` INT NOT NULL ,
  `schreiber_verbessert` TINYINT NULL ,
  `chassinat_verbessert` TINYINT NULL ,
  PRIMARY KEY (`uid_local`, `uid_foreign`) ,
  INDEX `fk_wort_has_stelle_stelle1_idx` (`uid_foreign` ASC) ,
  INDEX `fk_wort_has_stelle_wort1_idx` (`uid_local` ASC) )
ENGINE = MyISAM
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_unicode_ci;


-- -----------------------------------------------------
-- Table `edfu`.`ort_has_stelle`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `edfu`.`ort_has_stelle` ;

CREATE  TABLE IF NOT EXISTS `edfu`.`ort_has_stelle` (
  `uid_local` INT NOT NULL ,
  `uid_foreign` INT NOT NULL ,
  PRIMARY KEY (`uid_local`, `uid_foreign`) ,
  INDEX `fk_ort_has_stelle1_stelle1_idx` (`uid_foreign` ASC) ,
  INDEX `fk_ort_has_stelle1_ort1_idx` (`uid_local` ASC) )
ENGINE = MyISAM
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_unicode_ci;


-- -----------------------------------------------------
-- Table `edfu`.`szene_has_stelle`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `edfu`.`szene_has_stelle` ;

CREATE  TABLE IF NOT EXISTS `edfu`.`szene_has_stelle` (
  `uid_local` INT NOT NULL ,
  `uid_foreign` INT NOT NULL ,
  PRIMARY KEY (`uid_local`, `uid_foreign`) ,
  INDEX `fk_szene_has_stelle_stelle1_idx` (`uid_foreign` ASC) ,
  INDEX `fk_szene_has_stelle_szene1_idx` (`uid_local` ASC) ,
  CONSTRAINT `fk_szene_has_stelle_szene1`
    FOREIGN KEY (`uid_local` )
    REFERENCES `edfu`.`szene` (`uid` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_szene_has_stelle_stelle1`
    FOREIGN KEY (`uid_foreign` )
    REFERENCES `edfu`.`stelle` (`uid` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `edfu`.`formular_has_photo`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `edfu`.`formular_has_photo` ;

CREATE  TABLE IF NOT EXISTS `edfu`.`formular_has_photo` (
  `uid_local` INT NOT NULL ,
  `uid_foreign` INT NOT NULL ,
  `kommentar` TEXT NULL ,
  PRIMARY KEY (`uid_local`, `uid_foreign`) ,
  INDEX `fk_formular_has_photo_photo1_idx` (`uid_foreign` ASC) ,
  INDEX `fk_formular_has_photo_formular1_idx` (`uid_local` ASC) )
ENGINE = MyISAM
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_unicode_ci;



SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
