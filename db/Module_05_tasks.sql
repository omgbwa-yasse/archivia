CREATE TABLE `workflow_definitions` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(100) NOT NULL,
    `description` TEXT,
    `bpmn_xml` LONGTEXT NOT NULL,
    `version` INT NOT NULL DEFAULT 1,
    `status` VARCHAR(20) NOT NULL,
    `created_by` BIGINT NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_by` BIGINT,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    INDEX `idx_workflow_created` (`created_by`),
    INDEX `idx_workflow_updated` (`updated_by`),
    FOREIGN KEY (`created_by`) REFERENCES `users`(`id`),
    FOREIGN KEY (`updated_by`) REFERENCES `users`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `workflow_instances` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `definition_id` BIGINT NOT NULL,
    `name` VARCHAR(190) NOT NULL,
    `status` VARCHAR(20) NOT NULL,
    `current_state` JSON NOT NULL,
    `started_by` BIGINT NOT NULL,
    `started_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_by` BIGINT,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `completed_by` BIGINT,
    `completed_at` TIMESTAMP NULL,
    PRIMARY KEY (`id`),
    INDEX `idx_workflow_definition` (`definition_id`),
    INDEX `idx_workflow_started` (`started_by`),
    INDEX `idx_workflow_updated` (`updated_by`),
    INDEX `idx_workflow_completed` (`completed_by`),
    FOREIGN KEY (`definition_id`) REFERENCES `workflow_definitions`(`id`),
    FOREIGN KEY (`started_by`) REFERENCES `users`(`id`),
    FOREIGN KEY (`updated_by`) REFERENCES `users`(`id`),
    FOREIGN KEY (`completed_by`) REFERENCES `users`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `workflow_tasks` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `workflow_instance_id` BIGINT NOT NULL,
    `title` VARCHAR(190) NOT NULL,
    `description` TEXT,
    `status` VARCHAR(20) NOT NULL,
    `priority` VARCHAR(20) NOT NULL,
    `assigned_to` BIGINT,
    `due_date` TIMESTAMP NULL,
    `created_by` BIGINT NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_by` BIGINT,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `completed_by` BIGINT,
    `completed_at` TIMESTAMP NULL,
    PRIMARY KEY (`id`),
    INDEX `idx_task_workflow` (`workflow_instance_id`),
    INDEX `idx_task_assigned` (`assigned_to`),
    INDEX `idx_task_created` (`created_by`),
    INDEX `idx_task_updated` (`updated_by`),
    INDEX `idx_task_completed` (`completed_by`),
    FOREIGN KEY (`workflow_instance_id`) REFERENCES `workflow_instances`(`id`),
    FOREIGN KEY (`assigned_to`) REFERENCES `users`(`id`),
    FOREIGN KEY (`created_by`) REFERENCES `users`(`id`),
    FOREIGN KEY (`updated_by`) REFERENCES `users`(`id`),
    FOREIGN KEY (`completed_by`) REFERENCES `users`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `tasks` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `title` VARCHAR(190) NOT NULL,
    `description` TEXT,
    `status` VARCHAR(20) NOT NULL,
    `priority` VARCHAR(20) NOT NULL,
    `assigned_to` BIGINT,
    `workflow_instance_id` BIGINT, -- Ajout de la colonne manquante
    `due_date` TIMESTAMP NULL,
    `created_by` BIGINT NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_by` BIGINT,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `completed_by` BIGINT,
    `completed_at` TIMESTAMP NULL,
    PRIMARY KEY (`id`),
    INDEX `idx_task_workflow` (`workflow_instance_id`),
    INDEX `idx_task_assigned` (`assigned_to`),
    INDEX `idx_task_created` (`created_by`),
    INDEX `idx_task_updated` (`updated_by`),
    INDEX `idx_task_completed` (`completed_by`),
    FOREIGN KEY (`workflow_instance_id`) REFERENCES `workflow_instances`(`id`),
    FOREIGN KEY (`assigned_to`) REFERENCES `users`(`id`),
    FOREIGN KEY (`created_by`) REFERENCES `users`(`id`),
    FOREIGN KEY (`updated_by`) REFERENCES `users`(`id`),
    FOREIGN KEY (`completed_by`) REFERENCES `users`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;