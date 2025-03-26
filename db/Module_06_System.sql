CREATE TABLE `audit_logs` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `event_type` VARCHAR(50) NOT NULL,
    `entity_type` VARCHAR(50) NOT NULL,
    `entity_id` BIGINT NOT NULL,
    `action` VARCHAR(50) NOT NULL,
    `old_value` JSON,
    `new_value` JSON,
    `user_id` BIGINT NOT NULL,
    `ip_address` VARCHAR(45),
    `user_agent` VARCHAR(190),
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    INDEX `idx_audit_user` (`user_id`),
    INDEX `idx_audit_entity` (`entity_type`, `entity_id`),
    INDEX `idx_audit_created` (`created_at`),
    FOREIGN KEY (`user_id`) REFERENCES `users`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Configuration LDAP
CREATE TABLE `ldap_config` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(100) NOT NULL,
    `description` TEXT,
    `server_url` VARCHAR(255) NOT NULL,
    `port` INT NOT NULL DEFAULT 389,
    `use_ssl` BOOLEAN NOT NULL DEFAULT FALSE,
    `bind_dn` VARCHAR(255),
    `bind_password` VARCHAR(255) COMMENT 'Stocké chiffré',
    `search_base` VARCHAR(255) NOT NULL,
    `user_search_filter` VARCHAR(255) NOT NULL,
    `group_search_filter` VARCHAR(255),
    `user_id_attribute` VARCHAR(50) NOT NULL DEFAULT 'uid',
    `user_email_attribute` VARCHAR(50) NOT NULL DEFAULT 'mail',
    `user_display_name_attribute` VARCHAR(50) NOT NULL DEFAULT 'cn',
    `group_id_attribute` VARCHAR(50) NOT NULL DEFAULT 'cn',
    `group_member_attribute` VARCHAR(50) NOT NULL DEFAULT 'member',
    `enabled` BOOLEAN NOT NULL DEFAULT FALSE,
    `connection_timeout` INT NOT NULL DEFAULT 5000,
    `created_by` BIGINT NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_by` BIGINT,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_ldap_name` (`name`),
    FOREIGN KEY (`created_by`) REFERENCES `users`(`id`),
    FOREIGN KEY (`updated_by`) REFERENCES `users`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Mapping utilisateurs LDAP vers utilisateurs locaux
CREATE TABLE `ldap_user_mapping` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `ldap_config_id` BIGINT NOT NULL,
    `ldap_user_id` VARCHAR(255) NOT NULL,
    `local_user_id` BIGINT NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `last_sync_at` TIMESTAMP NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_ldap_user` (`ldap_config_id`, `ldap_user_id`),
    UNIQUE KEY `uk_local_user` (`ldap_config_id`, `local_user_id`),
    INDEX `idx_ldap_user_mapping` (`ldap_user_id`),
    INDEX `idx_local_user_mapping` (`local_user_id`),
    FOREIGN KEY (`ldap_config_id`) REFERENCES `ldap_config`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`local_user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Mapping groupes LDAP vers groupes locaux
CREATE TABLE `ldap_group_mapping` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `ldap_config_id` BIGINT NOT NULL,
    `ldap_group_id` VARCHAR(255) NOT NULL,
    `local_group_id` BIGINT NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `last_sync_at` TIMESTAMP NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_ldap_group` (`ldap_config_id`, `ldap_group_id`),
    UNIQUE KEY `uk_local_group` (`ldap_config_id`, `local_group_id`),
    INDEX `idx_ldap_group_mapping` (`ldap_group_id`),
    INDEX `idx_local_group_mapping` (`local_group_id`),
    FOREIGN KEY (`ldap_config_id`) REFERENCES `ldap_config`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`local_group_id`) REFERENCES `groups`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Journal de synchronisation LDAP
CREATE TABLE `ldap_sync_logs` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `ldap_config_id` BIGINT NOT NULL,
    `sync_type` ENUM('USERS', 'GROUPS', 'ALL') NOT NULL,
    `start_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `end_time` TIMESTAMP NULL,
    `status` ENUM('RUNNING', 'COMPLETED', 'FAILED') NOT NULL DEFAULT 'RUNNING',
    `total_items` INT DEFAULT 0,
    `items_processed` INT DEFAULT 0,
    `items_created` INT DEFAULT 0,
    `items_updated` INT DEFAULT 0,
    `items_deleted` INT DEFAULT 0,
    `items_failed` INT DEFAULT 0,
    `error_message` TEXT,
    `created_by` BIGINT,
    PRIMARY KEY (`id`),
    INDEX `idx_ldap_sync_config` (`ldap_config_id`),
    INDEX `idx_ldap_sync_status` (`status`),
    INDEX `idx_ldap_sync_time` (`start_time`),
    FOREIGN KEY (`ldap_config_id`) REFERENCES `ldap_config`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`created_by`) REFERENCES `users`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Configuration de sauvegardes
CREATE TABLE `backup_config` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(100) NOT NULL,
    `description` TEXT,
    `storage_type` ENUM('LOCAL', 'FTP', 'SFTP', 'S3', 'CLOUD') NOT NULL,
    `storage_path` VARCHAR(255) NOT NULL,
    `retention_days` INT NOT NULL DEFAULT 30,
    `max_backups` INT DEFAULT NULL,
    `include_files` BOOLEAN NOT NULL DEFAULT TRUE,
    `include_database` BOOLEAN NOT NULL DEFAULT TRUE,
    `compression_type` ENUM('NONE', 'GZIP', 'ZIP') NOT NULL DEFAULT 'GZIP',
    `encryption_enabled` BOOLEAN NOT NULL DEFAULT FALSE,
    `encryption_key` VARCHAR(255) COMMENT 'Stocké chiffré',
    `schedule_type` ENUM('MANUAL', 'DAILY', 'WEEKLY', 'MONTHLY') NOT NULL DEFAULT 'MANUAL',
    `schedule_time` TIME DEFAULT '00:00:00',
    `schedule_day` VARCHAR(20) COMMENT 'Jour de la semaine pour hebdomadaire, jour du mois pour mensuel',
    `enabled` BOOLEAN NOT NULL DEFAULT TRUE,
    `created_by` BIGINT NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_by` BIGINT,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_backup_name` (`name`),
    FOREIGN KEY (`created_by`) REFERENCES `users`(`id`),
    FOREIGN KEY (`updated_by`) REFERENCES `users`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Journal des sauvegardes
CREATE TABLE `backup_logs` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `backup_config_id` BIGINT NOT NULL,
    `filename` VARCHAR(255) NOT NULL,
    `file_size` BIGINT,
    `start_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `end_time` TIMESTAMP NULL,
    `status` ENUM('RUNNING', 'COMPLETED', 'FAILED') NOT NULL DEFAULT 'RUNNING',
    `type` ENUM('FULL', 'DATABASE', 'FILES') NOT NULL DEFAULT 'FULL',
    `storage_path` VARCHAR(255) NOT NULL,
    `error_message` TEXT,
    `includes_database` BOOLEAN NOT NULL DEFAULT TRUE,
    `includes_files` BOOLEAN NOT NULL DEFAULT TRUE,
    `is_compressed` BOOLEAN NOT NULL DEFAULT TRUE,
    `is_encrypted` BOOLEAN NOT NULL DEFAULT FALSE,
    `checksum` VARCHAR(64),
    `initiated_by` VARCHAR(50) NOT NULL DEFAULT 'SYSTEM' COMMENT 'SYSTEM ou ID utilisateur',
    `created_by` BIGINT,
    PRIMARY KEY (`id`),
    INDEX `idx_backup_config` (`backup_config_id`),
    INDEX `idx_backup_status` (`status`),
    INDEX `idx_backup_time` (`start_time`),
    FOREIGN KEY (`backup_config_id`) REFERENCES `backup_config`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`created_by`) REFERENCES `users`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Journal des restaurations
CREATE TABLE `restore_logs` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `backup_log_id` BIGINT NOT NULL,
    `start_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `end_time` TIMESTAMP NULL,
    `status` ENUM('RUNNING', 'COMPLETED', 'FAILED') NOT NULL DEFAULT 'RUNNING',
    `restore_type` ENUM('FULL', 'DATABASE', 'FILES', 'PARTIAL') NOT NULL,
    `restored_items` INT DEFAULT 0,
    `error_message` TEXT,
    `created_by` BIGINT NOT NULL,
    PRIMARY KEY (`id`),
    INDEX `idx_restore_backup` (`backup_log_id`),
    INDEX `idx_restore_status` (`status`),
    INDEX `idx_restore_time` (`start_time`),
    FOREIGN KEY (`backup_log_id`) REFERENCES `backup_logs`(`id`),
    FOREIGN KEY (`created_by`) REFERENCES `users`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

