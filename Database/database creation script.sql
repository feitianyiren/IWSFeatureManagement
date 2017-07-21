CREATE DATABASE `iwswebrequest` /*!40100 DEFAULT CHARACTER SET utf8 */;

CREATE TABLE `client` (
  `client_id` int(11) NOT NULL AUTO_INCREMENT,
  `client_name` varchar(255) NOT NULL,
  PRIMARY KEY (`client_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

CREATE TABLE `product_area` (
  `product_area_id` int(11) NOT NULL AUTO_INCREMENT,
  `product_area_name` varchar(255) NOT NULL,
  PRIMARY KEY (`product_area_id`),
  UNIQUE KEY `product_area_id_UNIQUE` (`product_area_id`),
  UNIQUE KEY `product_area_name_UNIQUE` (`product_area_name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

CREATE TABLE `feature_request` (
  `feature_request_id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `description` varchar(500) NOT NULL,
  `target_date` datetime NOT NULL,
  `product_area_id` int(11) NOT NULL,
  PRIMARY KEY (`feature_request_id`),
  KEY `feature_request_product_area_idx` (`product_area_id`),
  CONSTRAINT `feature_request_product_area` FOREIGN KEY (`product_area_id`) REFERENCES `product_area` (`product_area_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

CREATE TABLE `client_feature` (
  `client_id` int(11) NOT NULL,
  `feature_id` int(11) NOT NULL,
  `priority` int(11) NOT NULL,
  PRIMARY KEY (`client_id`,`feature_id`,`priority`),
  KEY `client_feature_client_idx` (`feature_id`),
  CONSTRAINT `client_feature_client` FOREIGN KEY (`client_id`) REFERENCES `client` (`client_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `client_feature_feature` FOREIGN KEY (`feature_id`) REFERENCES `feature_request` (`feature_request_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

insert into iwswebrequest.product_area (product_area_name) 
values('Policies'), ('Billing'),('Claims'),('Reports');

insert into iwswebrequest.client (client_name)
values ('Client A'), ('Client B'), ('Client C');

insert into iwswebrequest.feature_request (title, description, target_date, product_area_id)
values ('Feature 1', 'A new feature','2017-8-1',1);

insert into iwswebrequest.client_feature (client_id, feature_id, priority)
values (1,1,1);
