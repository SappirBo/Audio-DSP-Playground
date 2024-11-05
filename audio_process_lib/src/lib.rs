// use pyo3::prelude::*;
use numpy::ndarray::{ArrayD, ArrayViewD, ArrayViewMutD};
use numpy::{IntoPyArray, PyArrayDyn, PyReadonlyArrayDyn, PyArrayMethods};
use ndarray::prelude::*;
use pyo3::{pymodule, types::PyModule, PyResult, Python, Bound};


#[pymodule]
fn audio_process_lib<'py>(_py: Python<'py>, m: &Bound<'py, PyModule>) -> PyResult<()> {
    // example using a mutable borrow to modify an array in-place
    fn mult(a: f64, mut x: ArrayViewMutD<'_, f64>) {
        x *= a
    }

    // // wrapper of `axpy`
    // #[pyfn(m)]
    // #[pyo3(name = "axpy")]
    // fn axpy_py<'py>(
    //     py: Python<'py>,
    //     a: f64,
    //     x: PyReadonlyArrayDyn<'py, f64>,
    //     y: PyReadonlyArrayDyn<'py, f64>,
    // ) -> Bound<'py, PyArrayDyn<f64>> {
    //     let x = x.as_array();
    //     let y = y.as_array();
    //     let z = axpy(a, x, y);
    //     z.into_pyarray_bound(py)
    // }

    // // wrapper of `mult`
    #[pyfn(m)]
    #[pyo3(name = "mult")]
    fn mult_py<'py>(a: f64, x: &Bound<'py, PyArrayDyn<f64>>) {
        let x = unsafe { x.as_array_mut() };
        mult(a, x);
    }

    Ok(())
}
