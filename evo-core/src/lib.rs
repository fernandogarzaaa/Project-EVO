use pyo3::prelude::*;
use std::process::Command;

#[pyfunction]
fn invoke_swarm_agent(agent: String, task: String) -> PyResult<String> {
    let output = Command::new("python")
        .arg(format!("D:/project-evo/swarms/agents/{}.py", agent))
        .arg("--task")
        .arg(task)
        .output()
        .expect("Failed to execute agent");
        
    Ok(String::from_utf8_lossy(&output.stdout).to_string())
}

#[pymodule]
fn evo_core(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(invoke_swarm_agent, m)?)?;
    Ok(())
}
