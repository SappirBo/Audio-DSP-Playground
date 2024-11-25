use pyo3::prelude::*;
use numpy::PyReadwriteArrayDyn;


#[pyfunction]
pub fn process_overdrive<'py>(_py: Python<'py>, mut data: PyReadwriteArrayDyn<'py, f64>, _level:f64, mix: f64){
    for sample in data.as_array_mut().iter_mut(){
        let max_val = 1.0;
        let two_thirds = 0.66666;
        let third = 0.3333;

        if sample.abs() > two_thirds {
            *sample = (mix) * max_val + 
                        (1.0-mix) * *sample;
        }
        else if sample.abs() > third && sample.abs() <= two_thirds {
            *sample = (mix) * ((3.0 - (2.0 - 3.0 * *sample).powi(2))/3.0) + 
                        (1.0-mix) * *sample;
        }
        else{
            *sample = (mix) * ((*sample) * 2.0) + 
                        (1.0-mix) * *sample;
        }
    }
}

