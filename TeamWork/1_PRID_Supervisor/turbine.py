import hashlib
import json
import os

# PRID_1: Supervisor (Architect)
# Assigned to: Aditya Sadhu
# Scope: Core state engine and Software-Defined Integrity Guard (v1.0 Signed).

class IntegrityGuard:
    """
    Crucible Turbine Software-Defined Integrity Guard.
    Enforces 'Zero-Trust' isolation by verifying cryptographic hashes and signatures.
    """
    
    def __init__(self, registry_path="integrity_registry.json", secrets_path="auth_secrets.json"):
        self.registry_path = registry_path
        self.secrets_path = secrets_path
        self.registry = self._load_registry()
        self._verify_registry_signature()
    
    def _load_registry(self):
        if not os.path.exists(self.registry_path):
            raise FileNotFoundError(f"CRITICAL: Integrity Registry missing at {self.registry_path}")
        with open(self.registry_path, "r") as f:
            return json.load(f)
            
    def _verify_registry_signature(self):
        """Ensures the registry itself hasn't been tampered with."""
        if not os.path.exists(self.secrets_path):
             raise PermissionError("CRITICAL: Auth Secrets missing. Security compromised.")
             
        with open(self.secrets_path, "r") as f:
            master_key = json.load(f)["master_key"]
            
        data = self.registry.get("data")
        expected_sig = self.registry.get("metadata", {}).get("signature")
        
        if not data or not expected_sig:
            raise ValueError("CRITICAL: Registry format corruption detected.")
            
        content_str = json.dumps(data, sort_keys=True)
        current_sig = hashlib.sha256((content_str + master_key).encode()).hexdigest()
        
        if current_sig != expected_sig:
            raise SecurityError("CRITICAL: REGISTRY SIGNATURE MISMATCH! The security database has been tampered with!")

    def _get_current_hash(self, file_path):
        sha256 = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                while chunk := f.read(8192):
                    sha256.update(chunk)
            return sha256.hexdigest()
        except FileNotFoundError:
            return None

    def verify_zone(self, PRID):
        """Verifies all files assigned to a specific PRID."""
        data = self.registry["data"]
        if PRID not in data:
            return False, f"Unknown PRID: {PRID}"
        
        for rel_path, expected_hash in data[PRID].items():
            abs_path = os.path.join(os.getcwd(), rel_path)
            current_hash = self._get_current_hash(abs_path)
            
            if current_hash != expected_hash:
                return False, f"INTEGRITY BREACH in {PRID}: {rel_path} has been tampered with!"
        
        return True, f"{PRID} integrity verified."

    def verify_all(self):
        """Verifies the integrity of the entire project."""
        for PRID in self.registry["data"]:
            success, message = self.verify_zone(PRID)
            if not success:
                return False, message
        return True, "Full system integrity confirmed."

class SecurityError(Exception):
    pass

# --- WORK ZONE START ---

if __name__ == "__main__":
    print("--- Crucible Turbine: Initializing Signed Integrity Check ---")
    try:
        guard = IntegrityGuard()
        success, message = guard.verify_all()
        if success:
            print(f"[OK] {message}")
        else:
            print(f"[CRITICAL] {message}")
    except SecurityError as se:
        print(f"[ACCESS DENIED] {se}")
    except Exception as e:
        print(f"[ERROR] {e}")
