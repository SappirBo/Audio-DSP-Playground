use pyo3::prelude::*;
use numpy::PyReadwriteArrayDyn;

fn get_buffer_size(time:f32)->u32{
    let sample_rate:f32 = 44100.0;
    let buffer_size = sample_rate * time; 
    let buffer = buffer_size as u32;

    buffer
}

#[pyfunction]
pub fn process_digital_delay<'py>(_py: Python<'py>, mut data: PyReadwriteArrayDyn<'py, f64>, feedback:f32, time:f32, _level:f64, mix: f64){
    let buffer_size:u32 = get_buffer_size(time);
    let mut delay_buffer = vec![0.0 ; buffer_size as usize];
    let mut delay_index = 0;

    for sample in data.as_array_mut().iter_mut(){
        let new_sample = (mix) * delay_buffer[delay_index] +
            (1.0 - mix) * (*sample);
        *sample = new_sample;
        delay_buffer[delay_index] = new_sample * feedback as f64;
        delay_index += 1;
        if delay_index == buffer_size as usize{
            delay_index = 0;
        }
    }
}
