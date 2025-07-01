import logging
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.policies import DCAwareRoundRobinPolicy
from cassandra.cqlengine import connection
from app.core.config import settings

logger = logging.getLogger(__name__)


class CassandraManager:
    """Cassandra database connection manager"""
    
    def __init__(self):
        self.cluster = None
        self.session = None
    
    def connect(self):
        """Connect to Cassandra cluster"""
        try:
            # Set up authentication
            auth_provider = PlainTextAuthProvider(
                username=settings.CASSANDRA_USERNAME,
                password=settings.CASSANDRA_PASSWORD
            )
            
            # Connect to the Cassandra cluster
            self.cluster = Cluster(
                [settings.CASSANDRA_HOST],
                port=settings.CASSANDRA_PORT,
                auth_provider=auth_provider,
                load_balancing_policy=DCAwareRoundRobinPolicy(local_dc='datacenter1'),
                protocol_version=5
            )
            
            self.session = self.cluster.connect()
            
            # Create keyspace if not exists
            self.session.execute(f"""
                CREATE KEYSPACE IF NOT EXISTS {settings.CASSANDRA_KEYSPACE}
                WITH REPLICATION = {{
                    'class': 'SimpleStrategy',
                    'replication_factor': 1
                }}
            """)
            
            # Use the keyspace
            self.session.set_keyspace(settings.CASSANDRA_KEYSPACE)
            
            # Set up CQL engine connection
            connection.setup(
                [settings.CASSANDRA_HOST],
                settings.CASSANDRA_KEYSPACE,
                auth_provider=auth_provider,
                load_balancing_policy=DCAwareRoundRobinPolicy(local_dc='datacenter1'),
                protocol_version=5
            )
            
            logger.info("Successfully connected to Cassandra cluster")
            
        except Exception as e:
            logger.error(f"Failed to connect to Cassandra: {e}")
            raise
    
    def get_session(self):
        """Get Cassandra session"""
        if not self.session:
            self.connect()
        return self.session
    
    def close(self):
        """Close Cassandra connection"""
        try:
            if self.session:
                self.session.shutdown()
            if self.cluster:
                self.cluster.shutdown()
            logger.info("Cassandra connection closed")
        except Exception as e:
            logger.error(f"Error closing Cassandra connection: {e}")


# Global database manager instance
cassandra_manager = CassandraManager()


def get_cassandra_session():
    """Dependency to get Cassandra session"""
    return cassandra_manager.get_session()


def init_database():
    """Initialize database tables"""
    try:
        session = cassandra_manager.get_session()
        
        # Create tables
        create_tables(session)
        logger.info("Database tables initialized successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise


def create_tables(session):
    """Create all required tables"""
    
    # Sessions table
    session.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            mobile_no TEXT,
            device_id TEXT,
            session_token TEXT,
            user_id TEXT,
            jwt_token TEXT,
            fcm_token TEXT,
            created_at TIMESTAMP,
            expires_at TIMESTAMP,
            is_active BOOLEAN,
            updated_at TIMESTAMP,
            PRIMARY KEY ((mobile_no, device_id), created_at)
        ) WITH CLUSTERING ORDER BY (created_at DESC)
    """)
    
    # Users table
    session.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            mobile_no TEXT,
            email TEXT,
            full_name TEXT,
            state TEXT,
            referral_code TEXT,
            referred_by TEXT,
            profile_data TEXT,
            language_code TEXT,
            language_name TEXT,
            region_code TEXT,
            timezone TEXT,
            user_preferences TEXT,
            status TEXT,
            created_at TIMESTAMP,
            updated_at TIMESTAMP
        )
    """)
    
    # Games table
    session.execute("""
        CREATE TABLE IF NOT EXISTS games (
            id TEXT PRIMARY KEY,
            name TEXT,
            description TEXT,
            category TEXT,
            icon TEXT,
            banner TEXT,
            min_players INT,
            max_players INT,
            difficulty TEXT,
            rating DOUBLE,
            is_active BOOLEAN,
            is_featured BOOLEAN,
            tags LIST<TEXT>,
            metadata MAP<TEXT, TEXT>,
            created_at TEXT,
            updated_at TEXT
        )
    """)
    
    # Contests table
    session.execute("""
        CREATE TABLE IF NOT EXISTS contests (
            contest_id TEXT PRIMARY KEY,
            contest_name TEXT,
            contest_win_price TEXT,
            contest_entryfee TEXT,
            contest_joinuser INT,
            contest_activeuser INT,
            contest_starttime TEXT,
            contest_endtime TEXT
        )
    """)
    

    
    # OTP store table
    session.execute("""
        CREATE TABLE IF NOT EXISTS otp_store(
            phone_or_email text,      
            otp_code text,           
            created_at TEXT,     
            expires_at TEXT,     
            purpose text,            
            is_verified boolean,      
            attempt_count int,         
            PRIMARY KEY ((phone_or_email), purpose, created_at)
        ) WITH CLUSTERING ORDER BY (purpose ASC, created_at DESC)
    """)
    
    # League joins table
    session.execute("""
        CREATE TABLE IF NOT EXISTS league_joins (
            league_id TEXT,
            status TEXT,
            user_id TEXT,
            id UUID,
            joined_at TEXT,
            updated_at TEXT,
            invite_code TEXT,
            role TEXT,
            extra_data TEXT,
            status_id TEXT,
            PRIMARY KEY ((league_id, status), user_id, joined_at)
        ) WITH CLUSTERING ORDER BY (user_id ASC, joined_at DESC)
    """) 