CREATE TABLE `workspaces` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(100) NOT NULL,
    `description` TEXT,
    `owner_id` BIGINT NOT NULL,
    `root_folder_id` BIGINT NULL, -- Permettre NULL initialement pour éviter la référence circulaire
    `created_by` BIGINT NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_by` BIGINT,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `deleted_by` BIGINT,
    `deleted_at` TIMESTAMP NULL,
    PRIMARY KEY (`id`),
    INDEX `idx_workspace_owner` (`owner_id`),
    INDEX `idx_workspace_created` (`created_by`),
    INDEX `idx_workspace_updated` (`updated_by`),
    INDEX `idx_workspace_deleted` (`deleted_by`),
    FOREIGN KEY (`owner_id`) REFERENCES `users`(`id`),
    FOREIGN KEY (`created_by`) REFERENCES `users`(`id`),
    FOREIGN KEY (`updated_by`) REFERENCES `users`(`id`),
    FOREIGN KEY (`deleted_by`) REFERENCES `users`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `workspace_members` (
    `workspace_id` BIGINT NOT NULL,
    `user_id` BIGINT NOT NULL,
    `role` VARCHAR(50) NOT NULL,
    `created_by` BIGINT NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_by` BIGINT,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`workspace_id`, `user_id`),
    INDEX `idx_ws_member_created` (`created_by`),
    INDEX `idx_ws_member_updated` (`updated_by`),
    FOREIGN KEY (`workspace_id`) REFERENCES `workspaces`(`id`),
    FOREIGN KEY (`user_id`) REFERENCES `users`(`id`),
    FOREIGN KEY (`created_by`) REFERENCES `users`(`id`),
    FOREIGN KEY (`updated_by`) REFERENCES `users`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tables pour la gestion du calendrier et des événements
CREATE TABLE `calendars` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `workspace_id` BIGINT NOT NULL,
    `name` VARCHAR(100) NOT NULL,
    `description` TEXT,
    `color` VARCHAR(20),
    `is_default` BOOLEAN DEFAULT FALSE,
    `created_by` BIGINT NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_by` BIGINT,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `deleted_by` BIGINT,
    `deleted_at` TIMESTAMP NULL,
    PRIMARY KEY (`id`),
    INDEX `idx_calendar_workspace` (`workspace_id`),
    INDEX `idx_calendar_created` (`created_by`),
    INDEX `idx_calendar_updated` (`updated_by`),
    INDEX `idx_calendar_deleted` (`deleted_by`),
    FOREIGN KEY (`workspace_id`) REFERENCES `workspaces`(`id`),
    FOREIGN KEY (`created_by`) REFERENCES `users`(`id`),
    FOREIGN KEY (`updated_by`) REFERENCES `users`(`id`),
    FOREIGN KEY (`deleted_by`) REFERENCES `users`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `events` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `calendar_id` BIGINT NOT NULL,
    `title` VARCHAR(200) NOT NULL,
    `description` TEXT,
    `location` VARCHAR(255),
    `start_date` DATETIME NOT NULL,
    `end_date` DATETIME NOT NULL,
    `all_day` BOOLEAN DEFAULT FALSE,
    `recurrence_rule` VARCHAR(255),
    `priority` TINYINT DEFAULT 0,
    `status` VARCHAR(50) DEFAULT 'active',
    `created_by` BIGINT NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_by` BIGINT,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `deleted_by` BIGINT,
    `deleted_at` TIMESTAMP NULL,
    PRIMARY KEY (`id`),
    INDEX `idx_event_calendar` (`calendar_id`),
    INDEX `idx_event_dates` (`start_date`, `end_date`),
    INDEX `idx_event_created` (`created_by`),
    INDEX `idx_event_updated` (`updated_by`),
    INDEX `idx_event_deleted` (`deleted_by`),
    FOREIGN KEY (`calendar_id`) REFERENCES `calendars`(`id`),
    FOREIGN KEY (`created_by`) REFERENCES `users`(`id`),
    FOREIGN KEY (`updated_by`) REFERENCES `users`(`id`),
    FOREIGN KEY (`deleted_by`) REFERENCES `users`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `event_attendees` (
    `event_id` BIGINT NOT NULL,
    `user_id` BIGINT NOT NULL,
    `response_status` VARCHAR(50) DEFAULT 'pending', -- 'pending', 'accepted', 'declined', 'tentative'
    `notification_sent` BOOLEAN DEFAULT FALSE,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`event_id`, `user_id`),
    FOREIGN KEY (`event_id`) REFERENCES `events`(`id`),
    FOREIGN KEY (`user_id`) REFERENCES `users`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `event_reminders` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `event_id` BIGINT NOT NULL,
    `user_id` BIGINT NOT NULL,
    `reminder_time` INT NOT NULL, -- Temps en minutes avant l'événement
    `reminder_type` VARCHAR(50) DEFAULT 'notification', -- 'email', 'notification', 'sms'
    `sent` BOOLEAN DEFAULT FALSE,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    INDEX `idx_reminder_event` (`event_id`),
    INDEX `idx_reminder_user` (`user_id`),
    FOREIGN KEY (`event_id`) REFERENCES `events`(`id`),
    FOREIGN KEY (`user_id`) REFERENCES `users`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tables pour la gestion des dossiers et documents
CREATE TABLE `workspace_folders` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `workspace_id` BIGINT NOT NULL,
    `parent_folder_id` BIGINT,
    `name` VARCHAR(255) NOT NULL,
    `description` TEXT,
    `path` VARCHAR(1000),
    `created_by` BIGINT NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_by` BIGINT,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `deleted_by` BIGINT,
    `deleted_at` TIMESTAMP NULL,
    PRIMARY KEY (`id`),
    INDEX `idx_folder_workspace` (`workspace_id`),
    INDEX `idx_folder_parent` (`parent_folder_id`),
    INDEX `idx_folder_path` (`path`(255)),
    INDEX `idx_folder_created` (`created_by`),
    INDEX `idx_folder_updated` (`updated_by`),
    INDEX `idx_folder_deleted` (`deleted_by`),
    FOREIGN KEY (`workspace_id`) REFERENCES `workspaces`(`id`),
    FOREIGN KEY (`parent_folder_id`) REFERENCES `workspace_folders`(`id`),
    FOREIGN KEY (`created_by`) REFERENCES `users`(`id`),
    FOREIGN KEY (`updated_by`) REFERENCES `users`(`id`),
    FOREIGN KEY (`deleted_by`) REFERENCES `users`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Maintenant on peut ajouter la contrainte de clé étrangère sur root_folder_id
ALTER TABLE `workspaces` 
ADD CONSTRAINT `fk_workspace_root_folder` 
FOREIGN KEY (`root_folder_id`) REFERENCES `workspace_folders`(`id`);

CREATE TABLE `workspace_documents` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `folder_id` BIGINT NOT NULL,
    `name` VARCHAR(255) NOT NULL,
    `description` TEXT,
    `file_path` VARCHAR(1000),
    `file_size` BIGINT,
    `file_type` VARCHAR(100),
    `mime_type` VARCHAR(100),
    `version` INT DEFAULT 1,
    `is_locked` BOOLEAN DEFAULT FALSE,
    `locked_by` BIGINT,
    `locked_at` TIMESTAMP NULL,
    `created_by` BIGINT NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_by` BIGINT,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `deleted_by` BIGINT,
    `deleted_at` TIMESTAMP NULL,
    PRIMARY KEY (`id`),
    INDEX `idx_document_folder` (`folder_id`),
    INDEX `idx_document_name` (`name`),
    INDEX `idx_document_type` (`file_type`),
    INDEX `idx_document_locked` (`is_locked`),
    INDEX `idx_document_locked_by` (`locked_by`),
    INDEX `idx_document_created` (`created_by`),
    INDEX `idx_document_updated` (`updated_by`),
    INDEX `idx_document_deleted` (`deleted_by`),
    FOREIGN KEY (`folder_id`) REFERENCES `workspace_folders`(`id`),
    FOREIGN KEY (`locked_by`) REFERENCES `users`(`id`),
    FOREIGN KEY (`created_by`) REFERENCES `users`(`id`),
    FOREIGN KEY (`updated_by`) REFERENCES `users`(`id`),
    FOREIGN KEY (`deleted_by`) REFERENCES `users`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `workspace_document_versions` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `document_id` BIGINT NOT NULL,
    `version` INT NOT NULL,
    `file_path` VARCHAR(1000),
    `file_size` BIGINT,
    `change_summary` TEXT,
    `created_by` BIGINT NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_doc_version` (`document_id`, `version`),
    INDEX `idx_docver_document` (`document_id`),
    INDEX `idx_docver_created` (`created_by`),
    FOREIGN KEY (`document_id`) REFERENCES `workspace_documents`(`id`),
    FOREIGN KEY (`created_by`) REFERENCES `users`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `workspace_document_permissions` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `document_id` BIGINT NOT NULL,
    `user_id` BIGINT,
    `group_id` BIGINT,
    `permission_type` VARCHAR(50) NOT NULL, -- 'read', 'write', 'delete', 'share'
    `created_by` BIGINT NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_by` BIGINT,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    INDEX `idx_docperm_document` (`document_id`),
    INDEX `idx_docperm_user` (`user_id`),
    INDEX `idx_docperm_group` (`group_id`),
    INDEX `idx_docperm_created` (`created_by`),
    INDEX `idx_docperm_updated` (`updated_by`),
    FOREIGN KEY (`document_id`) REFERENCES `workspace_documents`(`id`),
    FOREIGN KEY (`user_id`) REFERENCES `users`(`id`),
    FOREIGN KEY (`group_id`) REFERENCES `groups`(`id`),
    FOREIGN KEY (`created_by`) REFERENCES `users`(`id`),
    FOREIGN KEY (`updated_by`) REFERENCES `users`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `workspace_document_shares` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `document_id` BIGINT NOT NULL,
    `share_token` VARCHAR(255) NOT NULL,
    `expires_at` TIMESTAMP NULL,
    `access_count` INT DEFAULT 0,
    `max_access_count` INT,
    `permission_type` VARCHAR(50) DEFAULT 'read', -- 'read', 'write'
    `password_protected` BOOLEAN DEFAULT FALSE,
    `password_hash` VARCHAR(255),
    `created_by` BIGINT NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_doc_share_token` (`share_token`),
    INDEX `idx_docshare_document` (`document_id`),
    INDEX `idx_docshare_expires` (`expires_at`),
    INDEX `idx_docshare_created` (`created_by`),
    FOREIGN KEY (`document_id`) REFERENCES `workspace_documents`(`id`),
    FOREIGN KEY (`created_by`) REFERENCES `users`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table pour lier les événements aux documents
CREATE TABLE `workspace_event_documents` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `event_id` BIGINT NOT NULL,
    `document_id` BIGINT NOT NULL,
    `attachment_type` VARCHAR(50) DEFAULT 'reference', -- 'reference', 'attachment', 'agenda', 'minutes'
    `created_by` BIGINT NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_by` BIGINT,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_event_document` (`event_id`, `document_id`, `attachment_type`),
    INDEX `idx_event_doc_event` (`event_id`),
    INDEX `idx_event_doc_document` (`document_id`),
    INDEX `idx_event_doc_created` (`created_by`),
    INDEX `idx_event_doc_updated` (`updated_by`),
    FOREIGN KEY (`event_id`) REFERENCES `events`(`id`),
    FOREIGN KEY (`document_id`) REFERENCES `workspace_documents`(`id`),
    FOREIGN KEY (`created_by`) REFERENCES `users`(`id`),
    FOREIGN KEY (`updated_by`) REFERENCES `users`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tables modifiées pour la gestion des transferts
-- Table pour gérer les liens entre documents (workspace/système)
CREATE TABLE `workspace_document_links` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `workspace_document_id` BIGINT NOT NULL,
    `system_document_id` BIGINT NOT NULL,
    `link_type` VARCHAR(50) NOT NULL, -- 'reference', 'copy', 'moved_from', 'moved_to'
    `last_sync_at` TIMESTAMP NULL, -- Date de dernière synchronisation
    `created_by` BIGINT NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_by` BIGINT,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_document_link` (`workspace_document_id`, `system_document_id`),
    INDEX `idx_ws_document` (`workspace_document_id`),
    INDEX `idx_system_document` (`system_document_id`),
    INDEX `idx_link_type` (`link_type`),
    FOREIGN KEY (`workspace_document_id`) REFERENCES `workspace_documents`(`id`),
    FOREIGN KEY (`system_document_id`) REFERENCES `documents`(`id`),
    FOREIGN KEY (`created_by`) REFERENCES `users`(`id`),
    FOREIGN KEY (`updated_by`) REFERENCES `users`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table pour lier dossiers d'espace de travail et dossiers système (sans hash)
CREATE TABLE `workspace_folder_links` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `workspace_folder_id` BIGINT NOT NULL,
    `system_folder_id` BIGINT NOT NULL,
    `link_type` VARCHAR(50) NOT NULL, -- 'reference', 'copy', 'moved_from', 'moved_to'
    `last_sync_at` TIMESTAMP NULL, -- Date de dernière synchronisation
    `created_by` BIGINT NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_by` BIGINT,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_folder_link` (`workspace_folder_id`, `system_folder_id`),
    INDEX `idx_ws_folder` (`workspace_folder_id`),
    INDEX `idx_system_folder` (`system_folder_id`),
    INDEX `idx_folder_link_type` (`link_type`),
    FOREIGN KEY (`workspace_folder_id`) REFERENCES `workspace_folders`(`id`),
    FOREIGN KEY (`system_folder_id`) REFERENCES `folders`(`id`),
    FOREIGN KEY (`created_by`) REFERENCES `users`(`id`),
    FOREIGN KEY (`updated_by`) REFERENCES `users`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table pour suivre les transferts de fichiers avec hash uniquement pour les fichiers
CREATE TABLE `workspace_file_transfers` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `workspace_document_id` BIGINT NOT NULL,
    `system_document_id` BIGINT NOT NULL,
    `transfer_direction` VARCHAR(20) NOT NULL, -- 'to_workspace', 'to_system'
    `transfer_type` VARCHAR(20) NOT NULL, -- 'copy', 'move', 'reference'
    `file_sha512` VARCHAR(128) NOT NULL, -- Empreinte SHA-512 du fichier transféré
    `file_size` BIGINT, -- Taille du fichier en octets
    `transfer_status` VARCHAR(20) NOT NULL DEFAULT 'completed', -- 'pending', 'in_progress', 'completed', 'failed'
    `transferred_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Moment du transfert
    `created_by` BIGINT NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    INDEX `idx_transfer_ws_doc` (`workspace_document_id`),
    INDEX `idx_transfer_sys_doc` (`system_document_id`),
    INDEX `idx_transfer_sha512` (`file_sha512`),
    INDEX `idx_transfer_status` (`transfer_status`),
    INDEX `idx_transfer_created` (`created_by`),
    FOREIGN KEY (`workspace_document_id`) REFERENCES `workspace_documents`(`id`),
    FOREIGN KEY (`system_document_id`) REFERENCES `documents`(`id`),
    FOREIGN KEY (`created_by`) REFERENCES `users`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

