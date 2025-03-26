-- =================================================================
-- MODULE: GESTION DES EMAILS
-- =================================================================

CREATE TABLE `email_templates` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(100) NOT NULL,
    `subject` VARCHAR(190) NOT NULL,
    `body_html` TEXT NOT NULL,
    `body_text` TEXT,
    `variables` JSON,
    `category` VARCHAR(50),
    `is_system` BOOLEAN DEFAULT FALSE,
    `created_by` BIGINT NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_by` BIGINT,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_email_template_name` (`name`),
    INDEX `idx_email_template_category` (`category`),
    INDEX `idx_email_template_created` (`created_by`),
    FOREIGN KEY (`created_by`) REFERENCES `users`(`id`),
    FOREIGN KEY (`updated_by`) REFERENCES `users`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `emails` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `sender_id` BIGINT,
    `sender_email` VARCHAR(190) NOT NULL,
    `sender_name` VARCHAR(100),
    `recipient_email` VARCHAR(190) NOT NULL,
    `recipient_name` VARCHAR(100),
    `cc` TEXT,
    `bcc` TEXT,
    `subject` VARCHAR(190) NOT NULL,
    `body_html` LONGTEXT,
    `body_text` LONGTEXT,
    `status` ENUM('DRAFT', 'PENDING', 'SENT', 'FAILED', 'DELIVERED', 'OPENED') NOT NULL,
    `priority` ENUM('LOW', 'NORMAL', 'HIGH') DEFAULT 'NORMAL',
    `template_id` BIGINT,
    `related_entity_type` VARCHAR(50),
    `related_entity_id` BIGINT,
    `error_message` TEXT,
    `sent_at` TIMESTAMP NULL,
    `opened_at` TIMESTAMP NULL,
    `created_by` BIGINT NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_by` BIGINT,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    INDEX `idx_email_sender` (`sender_id`),
    INDEX `idx_email_recipient` (`recipient_email`),
    INDEX `idx_email_template` (`template_id`),
    INDEX `idx_email_related` (`related_entity_type`, `related_entity_id`),
    INDEX `idx_email_status` (`status`),
    INDEX `idx_email_created` (`created_at`),
    INDEX `idx_email_sent` (`sent_at`),
    FOREIGN KEY (`sender_id`) REFERENCES `users`(`id`),
    FOREIGN KEY (`template_id`) REFERENCES `email_templates`(`id`),
    FOREIGN KEY (`created_by`) REFERENCES `users`(`id`),
    FOREIGN KEY (`updated_by`) REFERENCES `users`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `email_attachments` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `email_id` BIGINT NOT NULL,
    `document_id` BIGINT,
    `file_name` VARCHAR(190) NOT NULL,
    `file_size` BIGINT NOT NULL,
    `mime_type` VARCHAR(100) NOT NULL,
    `content_id` VARCHAR(190),
    `is_inline` BOOLEAN DEFAULT FALSE,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    INDEX `idx_attachment_email` (`email_id`),
    INDEX `idx_attachment_document` (`document_id`),
    FOREIGN KEY (`email_id`) REFERENCES `emails`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`document_id`) REFERENCES `documents`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =================================================================
-- MODULE: GESTION DES TAGS
-- =================================================================

CREATE TABLE `tag_categories` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(50) NOT NULL,
    `description` TEXT,
    `color` VARCHAR(7),
    `icon` VARCHAR(50),
    `is_system` BOOLEAN DEFAULT FALSE,
    `created_by` BIGINT NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_by` BIGINT,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_tag_category_name` (`name`),
    INDEX `idx_tag_category_created` (`created_by`),
    FOREIGN KEY (`created_by`) REFERENCES `users`(`id`),
    FOREIGN KEY (`updated_by`) REFERENCES `users`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `tags` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(50) NOT NULL,
    `slug` VARCHAR(50) NOT NULL,
    `description` TEXT,
    `color` VARCHAR(7),
    `icon` VARCHAR(50),
    `category_id` BIGINT,
    `created_by` BIGINT NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_by` BIGINT,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_tag_slug` (`slug`),
    INDEX `idx_tag_category` (`category_id`),
    INDEX `idx_tag_created` (`created_by`),
    FOREIGN KEY (`category_id`) REFERENCES `tag_categories`(`id`) ON DELETE SET NULL,
    FOREIGN KEY (`created_by`) REFERENCES `users`(`id`),
    FOREIGN KEY (`updated_by`) REFERENCES `users`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `taggable_entities` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `tag_id` BIGINT NOT NULL,
    `entity_type` VARCHAR(50) NOT NULL,
    `entity_id` BIGINT NOT NULL,
    `created_by` BIGINT NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_taggable_entity` (`tag_id`, `entity_type`, `entity_id`),
    INDEX `idx_taggable_tag` (`tag_id`),
    INDEX `idx_taggable_entity` (`entity_type`, `entity_id`),
    INDEX `idx_taggable_created` (`created_by`),
    FOREIGN KEY (`tag_id`) REFERENCES `tags`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`created_by`) REFERENCES `users`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

