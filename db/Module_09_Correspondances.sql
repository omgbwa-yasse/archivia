CREATE TABLE IF NOT EXISTS `batches` (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `code` varchar(10) NOT NULL,
  `name` varchar(250) NOT NULL,
  `organisation_holder_id` int UNSIGNED NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`organisation_holder_id`) REFERENCES `organisations` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE IF NOT EXISTS `batch_correspondence` (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `batch_id` int UNSIGNED NOT NULL,
  `correspondence_id` int UNSIGNED NOT NULL,
  `insert_date` datetime DEFAULT NULL,
  `remove_date` datetime DEFAULT NULL,
  `insert_by` int UNSIGNED NOT NULL,
  `insert_by_organisation_id` int UNSIGNED NOT NULL,
  `remove_by` int UNSIGNED DEFAULT NULL,
  `remove_by_organisation_id` int UNSIGNED DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`batch_id`) REFERENCES `batches` (`id`) ON DELETE CASCADE,
  FOREIGN KEY (`correspondence_id`) REFERENCES `correspondences` (`id`) ON DELETE CASCADE,
  FOREIGN KEY (`insert_by`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  FOREIGN KEY (`insert_by_organisation_id`) REFERENCES `organisations` (`id`) ON DELETE CASCADE,
  FOREIGN KEY (`remove_by`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  FOREIGN KEY (`remove_by_organisation_id`) REFERENCES `organisations` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;



CREATE TABLE IF NOT EXISTS `batch_transactions` (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `batch_id` int UNSIGNED NOT NULL,
  `send_by` int UNSIGNED NOT NULL,
  `send_by_organisation_id` int UNSIGNED NOT NULL,
  `send_to` int UNSIGNED NOT NULL,
  `send_to_organisation_id` int UNSIGNED NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`batch_id`) REFERENCES `batches` (`id`) ON DELETE CASCADE,
  FOREIGN KEY (`send_by`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  FOREIGN KEY (`send_to`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  FOREIGN KEY (`send_by_organisation_id`) REFERENCES `organisations` (`id`) ON DELETE CASCADE,
  FOREIGN KEY (`send_to_organisation_id`) REFERENCES `organisations` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;



CREATE TABLE IF NOT EXISTS `correspondences` (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `code` varchar(25) NOT NULL,
  `name` varchar(150) NOT NULL,
  `date` datetime NOT NULL,
  `description` text,
  `document_type` enum('original','duplicate','copy') NOT NULL DEFAULT 'original',
  `status` enum('draft','in_progress','transmitted','reject') NOT NULL DEFAULT 'draft',
  `priority_id` int UNSIGNED NOT NULL,
  `typology_id` int UNSIGNED NOT NULL,
  `action_id` int UNSIGNED NOT NULL,
  `sender_user_id` int UNSIGNED NOT NULL,
  `sender_organisation_id` int UNSIGNED NOT NULL,
  `recipient_user_id` int UNSIGNED DEFAULT NULL,
  `recipient_organisation_id` int UNSIGNED DEFAULT NULL,
  `is_archived` tinyint(1) NOT NULL DEFAULT '0',
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`priority_id`) REFERENCES `correspondence_priorities` (`id`) ON DELETE CASCADE,
  FOREIGN KEY (`typology_id`) REFERENCES `correspondence_typologies` (`id`) ON DELETE CASCADE,
  FOREIGN KEY (`action_id`) REFERENCES `correspondence_actions` (`id`) ON DELETE CASCADE,
  FOREIGN KEY (`sender_user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  FOREIGN KEY (`sender_organisation_id`) REFERENCES `organisations` (`id`) ON DELETE CASCADE,
  FOREIGN KEY (`recipient_user_id`) REFERENCES `users` (`id`) ON DELETE SET NULL,
  FOREIGN KEY (`recipient_organisation_id`) REFERENCES `organisations` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;



CREATE TABLE IF NOT EXISTS `correspondence_actions` (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `duration` int NOT NULL,
  `to_return` tinyint(1) NOT NULL DEFAULT '0',
  `description` text NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;



CREATE TABLE IF NOT EXISTS `correspondence_archives` (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `container_id` int UNSIGNED NOT NULL,
  `correspondence_id` int UNSIGNED NOT NULL,
  `archived_by` int UNSIGNED NOT NULL,
  `document_type` enum('original','duplicate','copy') NOT NULL DEFAULT 'original',
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`container_id`) REFERENCES `correspondence_containers` (`id`) ON DELETE CASCADE,
  FOREIGN KEY (`correspondence_id`) REFERENCES `correspondences` (`id`) ON DELETE CASCADE,
  FOREIGN KEY (`archived_by`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;




CREATE TABLE IF NOT EXISTS `correspondence_attachments` (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `correspondence_id` int UNSIGNED NOT NULL,
  `nom` varchar(255) NOT NULL,
  `hash` varchar(255) NOT NULL,
  `extension` varchar(50) NOT NULL,
  `nom_original` varchar(255) NOT NULL,
  `added_by` int UNSIGNED NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `correspondence_id` (`correspondence_id`),
  KEY `attachment_id` (`attachment_id`),
  KEY `added_by` (`added_by`),
  FOREIGN KEY (`correspondence_id`) REFERENCES `correspondences` (`id`) ON DELETE CASCADE,
  FOREIGN KEY (`added_by`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;



CREATE TABLE IF NOT EXISTS `correspondence_containers` (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `code` varchar(50) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `type_id` int UNSIGNED NOT NULL,
  `created_by` int UNSIGNED NOT NULL,
  `creator_organisation_id` int UNSIGNED NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`type_id`) REFERENCES `container_types` (`id`) ON DELETE CASCADE,
  FOREIGN KEY (`created_by`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  FOREIGN KEY (`creator_organisation_id`) REFERENCES `organisations` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE IF NOT EXISTS `correspondence_priorities` (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `duration` int NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE IF NOT EXISTS `correspondence_related` (
  `correspondence_id` int UNSIGNED NOT NULL,
  `correspondence_related_id` int UNSIGNED NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`correspondence_id`,`correspondence_related_id`),
  FOREIGN KEY (`correspondence_id`) REFERENCES `correspondences` (`id`) ON DELETE CASCADE,
  FOREIGN KEY (`correspondence_related_id`) REFERENCES `correspondences` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE IF NOT EXISTS `correspondence_typologies` (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `description` text,
  `activity_id` int UNSIGNED NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`activity_id`) REFERENCES `activities` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

