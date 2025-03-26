CREATE TABLE `folders` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(190) NOT NULL,
    `description` TEXT,
    `parent_id` BIGINT,
    `created_by` BIGINT NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_by` BIGINT,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `deleted_by` BIGINT,
    `deleted_at` TIMESTAMP NULL,
    `version` INT NOT NULL DEFAULT 1,
    `activity_id` BIGINT UNSIGNED NULL,
    PRIMARY KEY (`id`),
    INDEX `idx_folders_parent` (`parent_id`),
    INDEX `idx_folders_created` (`created_by`),
    INDEX `idx_folders_activity` (`activity_id`),
    FOREIGN KEY (`parent_id`) REFERENCES `folders`(`id`),
    FOREIGN KEY (`created_by`) REFERENCES `users`(`id`),
    FOREIGN KEY (`updated_by`) REFERENCES `users`(`id`),
    FOREIGN KEY (`deleted_by`) REFERENCES `users`(`id`),
    FOREIGN KEY (`activity_id`) REFERENCES `activities`(`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- Ajout de la colonne owner_id manquante dans la table documents
CREATE TABLE `documents` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(190) NOT NULL,
    `description` TEXT,
    `file_checksum` VARCHAR(190),
    `mime_type` VARCHAR(100) NOT NULL,
    `size` BIGINT NOT NULL,
    `folder_id` BIGINT NOT NULL,
    `owner_id` BIGINT NOT NULL,
    `created_by` BIGINT NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_by` BIGINT,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `deleted_by` BIGINT,
    `deleted_at` TIMESTAMP NULL,
    `version` INT NOT NULL DEFAULT 1,
    PRIMARY KEY (`id`),
    INDEX `idx_documents_folder` (`folder_id`),
    INDEX `idx_documents_owner` (`owner_id`),
    INDEX `idx_documents_created` (`created_by`),
    INDEX `idx_documents_updated` (`updated_by`),
    INDEX `idx_documents_deleted` (`deleted_by`),
    FOREIGN KEY (`folder_id`) REFERENCES `folders`(`id`),
    FOREIGN KEY (`owner_id`) REFERENCES `users`(`id`),
    FOREIGN KEY (`created_by`) REFERENCES `users`(`id`),
    FOREIGN KEY (`updated_by`) REFERENCES `users`(`id`),
    FOREIGN KEY (`deleted_by`) REFERENCES `users`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `document_versions` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `document_id` BIGINT NOT NULL,
    `version_number` INT NOT NULL,
    `file_checksum` VARCHAR(190) NOT NULL,
    `size` BIGINT NOT NULL,
    `created_by` BIGINT NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `comment` TEXT,
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_doc_version` (`document_id`, `version_number`),
    INDEX `idx_versions_created` (`created_by`),
    FOREIGN KEY (`document_id`) REFERENCES `documents`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`created_by`) REFERENCES `users`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `shared_documents` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `document_id` BIGINT NOT NULL,
    `file_checksum` VARCHAR(190) NOT NULL,
    `shared_by` BIGINT NOT NULL,
    `shared_with_user_id` BIGINT,
    `shared_with_email` VARCHAR(190),
    `access_type` ENUM('READ', 'WRITE', 'COMMENT') NOT NULL,
    `share_token` VARCHAR(190) UNIQUE,
    `token_used_at` TIMESTAMP NULL,
    `expiry_date` TIMESTAMP NULL,
    `max_views` INT,
    `view_count` INT DEFAULT 0,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `revoked_at` TIMESTAMP NULL,
    `revoked_by` BIGINT,
    `last_accessed_at` TIMESTAMP NULL,
    PRIMARY KEY (`id`),
    INDEX `idx_shared_doc` (`document_id`),
    INDEX `idx_shared_by` (`shared_by`),
    INDEX `idx_shared_with_user` (`shared_with_user_id`),
    INDEX `idx_share_token` (`share_token`),
    INDEX `idx_expiry` (`expiry_date`),
    FOREIGN KEY (`document_id`) REFERENCES `documents`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`shared_by`) REFERENCES `users`(`id`),
    FOREIGN KEY (`shared_with_user_id`) REFERENCES `users`(`id`),
    FOREIGN KEY (`revoked_by`) REFERENCES `users`(`id`),
    CONSTRAINT `chk_shared_with` CHECK (
        (`shared_with_user_id` IS NOT NULL AND `shared_with_email` IS NULL) OR
        (`shared_with_user_id` IS NULL AND `shared_with_email` IS NOT NULL)
    )
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `shared_folders` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `folder_id` BIGINT NOT NULL,
    `shared_by` BIGINT NOT NULL,
    `shared_with_user_id` BIGINT,
    `shared_with_email` VARCHAR(190),
    `access_type` ENUM('READ', 'WRITE', 'MANAGE') NOT NULL,
    `share_token` VARCHAR(190) UNIQUE,
    `token_used_at` TIMESTAMP NULL,
    `expiry_date` TIMESTAMP NULL,
    `max_views` INT,
    `view_count` INT DEFAULT 0,
    `include_subfolders` BOOLEAN DEFAULT FALSE,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `revoked_at` TIMESTAMP NULL,
    `revoked_by` BIGINT,
    `last_accessed_at` TIMESTAMP NULL,
    PRIMARY KEY (`id`),
    INDEX `idx_shared_folder` (`folder_id`),
    INDEX `idx_shared_by` (`shared_by`),
    INDEX `idx_shared_with_user` (`shared_with_user_id`),
    INDEX `idx_share_token` (`share_token`),
    INDEX `idx_expiry` (`expiry_date`),
    FOREIGN KEY (`folder_id`) REFERENCES `folders`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`shared_by`) REFERENCES `users`(`id`),
    FOREIGN KEY (`shared_with_user_id`) REFERENCES `users`(`id`),
    FOREIGN KEY (`revoked_by`) REFERENCES `users`(`id`),
    CONSTRAINT `chk_folder_shared_with` CHECK (
        (`shared_with_user_id` IS NOT NULL AND `shared_with_email` IS NULL) OR
        (`shared_with_user_id` IS NULL AND `shared_with_email` IS NOT NULL)
    )
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `metadata_definitions` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(50) NOT NULL,
    `description` TEXT,
    `data_type` VARCHAR(20) NOT NULL,
    `mandatory` BOOLEAN DEFAULT FALSE,
    `created_by` BIGINT NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_by` BIGINT,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    INDEX `idx_metadata_created` (`created_by`),
    INDEX `idx_metadata_updated` (`updated_by`),
    FOREIGN KEY (`created_by`) REFERENCES `users`(`id`),
    FOREIGN KEY (`updated_by`) REFERENCES `users`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `document_metadata` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `document_id` BIGINT NOT NULL,
    `definition_id` BIGINT NOT NULL,
    `value` TEXT,
    `created_by` BIGINT NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_by` BIGINT,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    INDEX `idx_doc_metadata` (`document_id`),
    INDEX `idx_metadata_definition` (`definition_id`),
    INDEX `idx_metadata_created` (`created_by`),
    INDEX `idx_metadata_updated` (`updated_by`),
    FOREIGN KEY (`document_id`) REFERENCES `documents`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`definition_id`) REFERENCES `metadata_definitions`(`id`),
    FOREIGN KEY (`created_by`) REFERENCES `users`(`id`),
    FOREIGN KEY (`updated_by`) REFERENCES `users`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `folder_metadata` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `folder_id` BIGINT NOT NULL,
    `definition_id` BIGINT NOT NULL,
    `value` TEXT,
    `created_by` BIGINT NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_by` BIGINT,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    INDEX `idx_folder_metadata` (`folder_id`),
    INDEX `idx_metadata_definition` (`definition_id`),
    INDEX `idx_metadata_created` (`created_by`),
    INDEX `idx_metadata_updated` (`updated_by`),
    FOREIGN KEY (`folder_id`) REFERENCES `folders`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`definition_id`) REFERENCES `metadata_definitions`(`id`),
    FOREIGN KEY (`created_by`) REFERENCES `users`(`id`),
    FOREIGN KEY (`updated_by`) REFERENCES `users`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `reference_lists` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(100) NOT NULL,
    `description` TEXT,
    `created_by` BIGINT NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_by` BIGINT,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_reference_list_name` (`name`),
    INDEX `idx_reflist_created` (`created_by`),
    INDEX `idx_reflist_updated` (`updated_by`),
    FOREIGN KEY (`created_by`) REFERENCES `users`(`id`),
    FOREIGN KEY (`updated_by`) REFERENCES `users`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `reference_values` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `list_id` BIGINT NOT NULL,
    `value` VARCHAR(190) NOT NULL,
    `description` TEXT,
    `active` BOOLEAN DEFAULT TRUE,
    `created_by` BIGINT NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_by` BIGINT,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    INDEX `idx_refval_list` (`list_id`),
    INDEX `idx_refval_created` (`created_by`),
    INDEX `idx_refval_updated` (`updated_by`),
    FOREIGN KEY (`list_id`) REFERENCES `reference_lists`(`id`),
    FOREIGN KEY (`created_by`) REFERENCES `users`(`id`),
    FOREIGN KEY (`updated_by`) REFERENCES `users`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Ajouter une table les annoations et commentaires