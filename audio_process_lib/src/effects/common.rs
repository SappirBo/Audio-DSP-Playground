use pyo3::prelude::*;
use numpy::PyReadwriteArrayDyn;

#[pyfunction]
pub fn process_levels<'py>(mut data: PyReadwriteArrayDyn<'py, f64>, level:f64){
    
    let factor:f64 = level / 10.0; 

    for sample in data.as_array_mut().iter_mut(){
        *sample = factor * (*sample)
    }
}
