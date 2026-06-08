from contextlib import contextmanager


class BaseRepository:
    @contextmanager
    def _session(self):
        from app.database import db_config

        # 1. Testes injetam uma factory específica
        if db_config._override_session_factory is not None:
            Factory = db_config._override_session_factory

        # 2. Visitante usa banco zerado separado
        else:
            try:
                from flask import has_request_context
                from flask import session as flask_session
                is_visitor = has_request_context() and flask_session.get("visitante", False)
            except RuntimeError:
                is_visitor = False

            Factory = db_config.VisitorSessionLocal if is_visitor else db_config.SessionLocal

        session = Factory()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
