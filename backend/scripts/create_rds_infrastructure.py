#!/usr/bin/env python3
"""
AWS RDS インフラストラクチャ作成スクリプト
プログラミング学習アプリ用のRDSインスタンスとセキュリティグループを作成
"""

import boto3
import json
import time
import logging
from typing import Dict, Any, Optional

# ログ設定
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# AWS設定
REGION = 'ap-northeast-1'
VPC_ID = 'vpc-0a2ad8c64d54453a6'
SUBNET_GROUP_NAME = 'csr-lambda-api-dev-subnet-group'

# RDS設定
DB_INSTANCE_IDENTIFIER = 'programming-learning-app-db'
DB_NAME = 'programming_learning_app'
DB_USERNAME = 'admin'
DB_PASSWORD = 'ProgrammingApp2024!'  # 本番環境では環境変数から取得
DB_INSTANCE_CLASS = 'db.t3.micro'  # 開発環境用の小さなインスタンス
ALLOCATED_STORAGE = 20
ENGINE = 'mysql'
ENGINE_VERSION = '8.0.35'

# セキュリティグループ設定
SECURITY_GROUP_NAME = 'programming-learning-app-rds-sg'
SECURITY_GROUP_DESCRIPTION = 'Security group for Programming Learning App RDS instance'

def create_security_group() -> Optional[str]:
    """
    RDS用のセキュリティグループを作成
    """
    try:
        ec2 = boto3.client('ec2', region_name=REGION)
        
        # セキュリティグループの作成
        response = ec2.create_security_group(
            GroupName=SECURITY_GROUP_NAME,
            Description=SECURITY_GROUP_DESCRIPTION,
            VpcId=VPC_ID
        )
        
        security_group_id = response['GroupId']
        logger.info(f"セキュリティグループを作成しました: {security_group_id}")
        
        # MySQL/Aurora用のインバウンドルールを追加（ポート3306）
        ec2.authorize_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=[
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 3306,
                    'ToPort': 3306,
                    'IpRanges': [
                        {
                            'CidrIp': '0.0.0.0/0',  # 開発環境用（本番では制限する）
                            'Description': 'MySQL access for development'
                        }
                    ]
                }
            ]
        )
        
        logger.info("セキュリティグループにMySQLアクセスルールを追加しました")
        
        # タグを追加
        ec2.create_tags(
            Resources=[security_group_id],
            Tags=[
                {'Key': 'Name', 'Value': SECURITY_GROUP_NAME},
                {'Key': 'Project', 'Value': 'programming-learning-app'},
                {'Key': 'Environment', 'Value': 'development'}
            ]
        )
        
        return security_group_id
        
    except Exception as e:
        logger.error(f"セキュリティグループ作成エラー: {str(e)}")
        return None

def create_rds_instance(security_group_id: str) -> bool:
    """
    RDSインスタンスを作成
    """
    try:
        rds = boto3.client('rds', region_name=REGION)
        
        # RDSインスタンスの作成
        response = rds.create_db_instance(
            DBInstanceIdentifier=DB_INSTANCE_IDENTIFIER,
            DBName=DB_NAME,
            DBInstanceClass=DB_INSTANCE_CLASS,
            Engine=ENGINE,
            EngineVersion=ENGINE_VERSION,
            MasterUsername=DB_USERNAME,
            MasterUserPassword=DB_PASSWORD,
            AllocatedStorage=ALLOCATED_STORAGE,
            VpcSecurityGroupIds=[security_group_id],
            DBSubnetGroupName=SUBNET_GROUP_NAME,
            BackupRetentionPeriod=7,  # 7日間のバックアップ保持
            MultiAZ=False,  # 開発環境では単一AZ
            PubliclyAccessible=True,  # 開発環境では外部アクセス可能
            StorageType='gp2',
            StorageEncrypted=True,
            DeletionProtection=False,  # 開発環境では削除保護無効
            Tags=[
                {'Key': 'Name', 'Value': DB_INSTANCE_IDENTIFIER},
                {'Key': 'Project', 'Value': 'programming-learning-app'},
                {'Key': 'Environment', 'Value': 'development'}
            ]
        )
        
        logger.info(f"RDSインスタンスの作成を開始しました: {DB_INSTANCE_IDENTIFIER}")
        logger.info("インスタンスが利用可能になるまで数分かかります...")
        
        return True
        
    except Exception as e:
        logger.error(f"RDSインスタンス作成エラー: {str(e)}")
        return False

def wait_for_db_instance() -> Optional[Dict[str, Any]]:
    """
    RDSインスタンスが利用可能になるまで待機
    """
    try:
        rds = boto3.client('rds', region_name=REGION)
        
        logger.info("RDSインスタンスの起動を待機中...")
        
        while True:
            response = rds.describe_db_instances(
                DBInstanceIdentifier=DB_INSTANCE_IDENTIFIER
            )
            
            db_instance = response['DBInstances'][0]
            status = db_instance['DBInstanceStatus']
            
            logger.info(f"現在のステータス: {status}")
            
            if status == 'available':
                logger.info("RDSインスタンスが利用可能になりました！")
                return db_instance
            elif status in ['failed', 'incompatible-parameters', 'incompatible-restore']:
                logger.error(f"RDSインスタンスの作成に失敗しました: {status}")
                return None
            
            time.sleep(30)  # 30秒待機
            
    except Exception as e:
        logger.error(f"RDSインスタンス待機エラー: {str(e)}")
        return None

def get_connection_info(db_instance: Dict[str, Any]) -> Dict[str, str]:
    """
    データベース接続情報を取得
    """
    endpoint = db_instance['Endpoint']['Address']
    port = db_instance['Endpoint']['Port']
    
    connection_info = {
        'host': endpoint,
        'port': str(port),
        'database': DB_NAME,
        'username': DB_USERNAME,
        'password': DB_PASSWORD
    }
    
    return connection_info

def create_env_file(connection_info: Dict[str, str]):
    """
    .env ファイルを作成
    """
    env_content = f"""# データベース設定（AWS RDS）
DATABASE_HOST={connection_info['host']}
DATABASE_PORT={connection_info['port']}
DATABASE_NAME={connection_info['database']}
DATABASE_USER={connection_info['username']}
DATABASE_PASSWORD={connection_info['password']}

# AWS設定
AWS_REGION={REGION}

# セキュリティ設定
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS設定
ALLOWED_ORIGINS=http://localhost:3000,https://localhost:3000
"""
    
    with open('.env', 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    logger.info(".env ファイルを作成しました")

def main():
    """
    メイン処理
    """
    print("=" * 60)
    print("AWS RDS インフラストラクチャ作成")
    print("=" * 60)
    
    # 1. セキュリティグループの作成
    print("\n1. セキュリティグループの作成...")
    security_group_id = create_security_group()
    if not security_group_id:
        print("✗ セキュリティグループの作成に失敗しました")
        return
    print(f"✓ セキュリティグループを作成しました: {security_group_id}")
    
    # 2. RDSインスタンスの作成
    print("\n2. RDSインスタンスの作成...")
    if not create_rds_instance(security_group_id):
        print("✗ RDSインスタンスの作成に失敗しました")
        return
    print("✓ RDSインスタンスの作成を開始しました")
    
    # 3. RDSインスタンスの起動待機
    print("\n3. RDSインスタンスの起動待機...")
    db_instance = wait_for_db_instance()
    if not db_instance:
        print("✗ RDSインスタンスの起動に失敗しました")
        return
    print("✓ RDSインスタンスが起動しました")
    
    # 4. 接続情報の取得と表示
    print("\n4. 接続情報の取得...")
    connection_info = get_connection_info(db_instance)
    
    print("\n" + "=" * 60)
    print("RDS接続情報")
    print("=" * 60)
    print(f"ホスト: {connection_info['host']}")
    print(f"ポート: {connection_info['port']}")
    print(f"データベース名: {connection_info['database']}")
    print(f"ユーザー名: {connection_info['username']}")
    print(f"パスワード: {connection_info['password']}")
    
    # 5. .env ファイルの作成
    print("\n5. .env ファイルの作成...")
    create_env_file(connection_info)
    print("✓ .env ファイルを作成しました")
    
    print("\n" + "=" * 60)
    print("RDSインフラストラクチャの作成が完了しました！")
    print("\n次のステップ:")
    print("1. python setup_rds_database.py を実行してテーブルを作成")
    print("2. python insert_sample_data_rds.py を実行してサンプルデータを投入")
    print("=" * 60)

if __name__ == "__main__":
    main()