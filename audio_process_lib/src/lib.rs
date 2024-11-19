use pyo3::prelude::*;
pub mod effects;
use numpy::PyReadwriteArrayDyn;


fn ms_to_bits(ms:f64)->i32{
    let sample_rate = 44100.0;
    let one_second = 1000.0;
    let ms_in_seconds = ms/one_second;
    let ms_in_bits = sample_rate*ms_in_seconds;
    return ms_in_bits as i32;
}

#[pyfunction]
fn compress<'py>(_py: Python<'py>, mut data: PyReadwriteArrayDyn<'py,f64>, threshold:f64, ratio: f64, attack:f64, release:f64){
        let bits_to_attack = ms_to_bits(attack);
        let bits_to_release = ms_to_bits(release);

        let threshold_range = 100.0;
        let sample_threashold = threshold / threshold_range;

        // Setup the counters
        let mut apply_compression = false;
        let mut attack_counter = 0;
        let mut release_counter = 0;
        // let mut refinement = 0.0;

        for sample in data.as_array_mut().iter_mut(){
            // check if sample trigers compressor - if it is -> reset counters
            if sample.abs() >= sample_threashold.abs() {
               if apply_compression == false {
                    apply_compression = true;
                    attack_counter = 0;
               }
               release_counter = 0;
            }
            
            // If the compressor has been trigered
            if apply_compression == true{
                if attack_counter <= bits_to_attack{
                    let refinement = attack_counter as f64/ bits_to_attack as f64;
                    let mut decrease = *sample/ratio;
                    let factor = if ratio * refinement > 1.0 {1.0} else{ ratio * refinement};
                    if ratio > 1.0{
                        decrease = *sample / factor;
                    }
                    *sample = decrease;
                    attack_counter += 1;
                }
                else if release_counter <= bits_to_release {
                    
                }
                else {
                    apply_compression = false; 
                }
            }
        }

        // let factor = 1.0/ratio;
        // for sample in data.as_array_mut().iter_mut() {
        //     *sample *=  factor ;
        // }
}


#[pymodule]
fn audio_process_lib<'py>(_py: Python<'py>, m: &Bound<'py, PyModule>) -> PyResult<()> {
    // example using a mutable borrow to modify an array in-place
    m.add_function(wrap_pyfunction!(compress, m)?)?;
    m.add_function(wrap_pyfunction!(effects::common::process_levels, m)?)?;
    m.add_function(wrap_pyfunction!(effects::overdrive::process_overdrive, m)?)?;
    m.add_function(wrap_pyfunction!(effects::digital_delay::process_digital_delay, m)?)?;
    Ok(())
}
