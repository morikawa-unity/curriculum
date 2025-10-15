-- ユーザー実績テーブルの作成（MySQL版）
-- 実行日: 2024-10-14

-- user_achievementsテーブルの作成
CREATE TABLE IF NOT EXISTS user_achievements (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    achievement_name VARCHAR(255) NOT NULL,
    achievement_description TEXT,
    earned_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- 外部キー制約
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    
    -- 同じユーザーが同じ実績を重複して獲得しないようにする
    UNIQUE KEY unique_user_achievement (user_id, achievement_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックスの作成
CREATE INDEX idx_user_achievements_user_id ON user_achievements(user_id);
CREATE INDEX idx_user_achievements_earned_date ON user_achievements(earned_date);

-- テーブルコメントの追加
ALTER TABLE user_achievements COMMENT = 'ユーザーの実績・バッジ情報を管理するテーブル';

-- サンプルデータの挿入（開発環境用）
INSERT IGNORE INTO user_achievements (user_id, achievement_name, achievement_description) 
SELECT 
    id,
    '新規登録',
    'アカウントを作成しました'
FROM users;