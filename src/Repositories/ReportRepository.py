from typing import Optional, List, Type

import pandas as pd
from sqlalchemy import or_, func

from src.Database.Database import Database
from src.Models.Dataset import Dataset
from src.Models.Report import Report
from src.Models.User import User


class ReportRepository:
    def __init__(self):
        self.db_session = Database().get_db()

    def create(self, data: dict) -> Report:
        """Cria um novo relatorio no banco de dados."""
        report = Report(**data)
        self.db_session.add(report)
        self.db_session.commit()
        self.db_session.refresh(report)
        return report

    def get_by_id(self, report_id: int) -> Optional[Report]:
        """Retorna um relatorio pelo ID."""
        return self.db_session.query(Report).filter(Report.id == report_id).first()

    def get_all(self, search: str) -> pd.DataFrame:
        query = self.db_session.query(Report, User, Dataset).join(User, User.id == Report.user_id) \
            .join(Dataset, Dataset.id == Report.dataset_id)

        query = query.with_entities(
            Report.id, Report.name, Report.description, User.name.label("user_name"), User.email.label("user_email"),
            Dataset.name.label("dataset_name")
        )

        if search:
            query = query.filter(
                or_(
                    func.lower(User.name).like(f"%{search.lower()}%"),
                    func.lower(User.email).like(f"%{search.lower()}%"),
                    func.lower(Report.name).like(f"%{search.lower()}%"),
                    func.lower(Report.description).like(f"%{search.lower()}%"),
                    func.lower(Dataset.name).like(f"%{search.lower()}%"),
                )
            )

        query = query.limit(30)

        return pd.read_sql(query.statement, self.db_session.bind)

    def update(self, report_id: int, data: dict) -> Optional[Report]:
        report = self.get_by_id(report_id)
        if report:
            for key, value in data.items():
                setattr(report, key, value)
            self.db_session.commit()
            self.db_session.refresh(report)
        return report
