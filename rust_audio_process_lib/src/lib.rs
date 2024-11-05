
use ndarray::ArrayViewMut1;
use numpy::{IntoPyArray, PyArray1};
use pyo3::prelude::*;

#[pyfunction]
fn apply_effect(py: Python, input_array: &PyArray1<f32>) -> Py<PyArray1<f32>> {
    // Convert the input PyArray to an ndarray
    let mut array = input_array.readonly().as_array().to_owned();
    let gain = 1.5;
    array *= gain;

    // Return the processed array back to Python
    array.into_pyarray(py).to_owned()
}

#[pymodule]
fn rust_audio_effects(py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(apply_effect, m)?)?;
    Ok(())
}
