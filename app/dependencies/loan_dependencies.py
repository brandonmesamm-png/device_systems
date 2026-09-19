"""
Módulo loan_dependencies
---------------------------
Funciones reutilizables con Depends() para el recurso "loans".
"""

from fastapi import Path, Depends
from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db
from app.models.loan_model import Loan
from app.services.loan_service import get_loan_by_id


def get_loan_or_404(
    loan_id: int = Path(..., description="ID del préstamo", gt=0),
    db: Session = Depends(get_db),
) -> Loan:
    """
    Dependencia que obtiene un préstamo por su ID (con user y device
    ya cargados). Si no existe, detiene la petición con un error 404.
    """
    return get_loan_by_id(db, loan_id)