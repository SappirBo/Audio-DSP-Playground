use pyo3::prelude::*;
use numpy::PyReadwriteArrayDyn;

#[pyfunction]
pub fn set_levels<'py>(mut data: PyReadwriteArrayDyn<'py, f64>, level:f64){
    for sample in data.as_array_mut().iter_mut(){
        *sample = level * (*sample)
    }
}
