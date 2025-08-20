import os
import yaml
import importlib

# Simple store for results between steps
results = {}

def load_module(module_name):
    """Dynamically import a module from modules/"""
    module_path = f"modules.{module_name}"
    try:
        return importlib.import_module(module_path)
    except ModuleNotFoundError:
        print(f"[!] Module {module_name} not found")
        return None

def run_workflow(workflow_file, target):
    with open(workflow_file, "r") as f:
        workflow = yaml.safe_load(f)

    print(f"[*] Running workflow: {workflow.get('workflow')}")
    
    for step in workflow["steps"]:
        module_name = step["module"]
        func_name = step["function"]
        depends_on = step.get("depends_on")
        params = step.get("params", {})

        # If step depends on another, pass its output
        input_data = results.get(depends_on) if depends_on else {"target": target}

        module = load_module(module_name)
        if not module:
            continue

        func = getattr(module, func_name, None)
        if not func:
            print(f"[!] Function {func_name} not found in module {module_name}")
            continue

        print(f"[*] Executing step: {step['name']} (module: {module_name})")
        try:
            output = func(input_data, **params)
            results[step["name"]] = output
        except Exception as e:
            print(f"[!] Error in step {step['name']}: {e}")

    print("[*] Workflow finished.")
    return results

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="WebFang Workflow Orchestrator")
    parser.add_argument("--workflow", required=True, help="Path to workflow YAML")
    parser.add_argument("--target", required=True, help="Target domain/IP")
    args = parser.parse_args()

    run_workflow(args.workflow, args.target)
