import sys
import subprocess
from pathlib import Path


def check_python_version():
    """Vérifier la version de Python"""
    version = sys.version_info
    print(f" Python: {version.major}.{version.minor}.{version.micro}", end=" ")
    
    if version.major >= 3 and version.minor >= 9:
        print("✓")
        return True
    else:
        print("✗ (3.9+ requis)")
        return False


def check_package(package_name, import_name=None):
    """Vérifier si un package est installé"""
    if import_name is None:
        import_name = package_name.replace("-", "_")
    
    try:
        __import__(import_name)
        print(f" {package_name}: ✓")
        return True
    except ImportError:
        print(f" {package_name}: ✗")
        return False


def check_file_exists(filepath):
    """Vérifier si un fichier existe"""
    if Path(filepath).exists():
        print(f" {filepath}: ✓")
        return True
    else:
        print(f" {filepath}: ✗")
        return False


def check_postgresql():
    """Vérifier PostgreSQL"""
    try:
        result = subprocess.run(
            ["psql", "--version"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f" PostgreSQL: ✓")
            return True
    except FileNotFoundError:
        pass
    
    print(f" PostgreSQL: ✗ (optionnel)")
    return False


def main():
    print("\n Diagnostic CacaoDetect Backend\n")
    
    checks = []
    
    # Vérifications importantes
    print(" Vérifications importantes:")
    checks.append(check_python_version())
    
    print("\n Packages Python:")
    essential_packages = [
        ("fastapi", "fastapi"),
        ("uvicorn", "uvicorn"),
        ("sqlalchemy", "sqlalchemy"),
        ("pydantic", "pydantic"),
        ("python-jose", "jose"),
        ("passlib", "passlib"),
        ("pyjwt", "jwt"),
        ("python-multipart", "multipart"),
    ]
    
    for package, import_name in essential_packages:
        checks.append(check_package(package, import_name))
    
    print("\n📁 Fichiers de configuration:")
    files_to_check = [
        ".env",
        ".env.example",
        "requirements.txt",
        "app/main.py",
    ]
    
    for filepath in files_to_check:
        checks.append(check_file_exists(filepath))
    
    print("\n  Base de données:")
    check_postgresql()  # Optionnel
    
    # Résumé
    print("\n" + "="*50)
    passed = sum(checks)
    total = len(checks)
    
    if all(checks):
        print(f"✓ Tous les vérifications passées ({passed}/{total})")
        print("\nVous pouvez démarrer le backend avec:")
        print("  python startup.py")
        return 0
    else:
        print(f" {passed}/{total} vérifications passées")
        print("\nProblèmes détectés:")
        print("  1. Installer les packages manquants:")
        print("     pip install -r requirements.txt")
        print("  2. Configurer .env:")
        print("     cp .env.example .env")
        return 1


if __name__ == "__main__":
    sys.exit(main())
