// use pyo3::prelude::*;
use numpy::ndarray::{ArrayViewMutD};
use numpy::{PyArrayDyn, PyArrayMethods};
use pyo3::{pymodule, types::PyModule, PyResult, Python, Bound};


#[pymodule]
fn audio_process_lib<'py>(_py: Python<'py>, m: &Bound<'py, PyModule>) -> PyResult<()> {
    // example using a mutable borrow to modify an array in-place
    fn mult(a: f64, mut x: ArrayViewMutD<'_, f64>) {
        x *= (1.0 / (10.0 * a))
    }


    // // wrapper of `mult`
    #[pyfn(m)]
    #[pyo3(name = "mult")]
    fn mult_py<'py>(a: f64, x: &Bound<'py, PyArrayDyn<f64>>) {
        let x = unsafe { x.as_array_mut() };
        mult(a, x);
    }

    Ok(())
}
