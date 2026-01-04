import numpy as np
import librosa
import soundfile as sf
import noisereduce as nr


def crossfade_arrays(array1, array2, overlap_samples):
    """
    Manually crossfades two numpy arrays.
    fades out the end of array1 and fades in the start of array2.
    """
    # Create fade curves (linear)
    fade_out = np.linspace(1, 0, overlap_samples)
    fade_in = np.linspace(0, 1, overlap_samples)

    # Slice the overlapping parts
    a1_overlap = array1[-overlap_samples:]
    a2_overlap = array2[:overlap_samples]

    # Apply fades
    faded_overlap = (a1_overlap * fade_out) + (a2_overlap * fade_in)

    # Concatenate: [Start of 1] + [Crossfade] + [End of 2]
    return np.concatenate(
        [array1[:-overlap_samples], faded_overlap, array2[overlap_samples:]]
    )


def process_audio():
    input_file = "new-york-stock-exchange-bell.mp3"
    output_file = "processed_bell_modern.wav"  # Saving as wav is safer with SoundFile

    print(f"Loading {input_file} via Librosa...")
    # Librosa loads as a floating point numpy array, normalized between -1 and 1
    # sr=None preserves the native sampling rate
    y, sr = librosa.load(input_file, sr=None)

    # --- 1. SLICING (NumPy) ---
    # Convert seconds to sample indices
    idx_10s = 10 * sr
    idx_3s = 3 * sr

    # Create the two segments
    segment_loop = y[:idx_10s]
    segment_end = y[-idx_3s:]

    # --- 2. CROSSFADE ---
    # We need an overlap. 50ms is standard for "de-clicking"
    crossfade_ms = 50
    overlap_samples = int((crossfade_ms / 1000) * sr)

    # We need to make sure we have enough audio to crossfade
    # (Borrowing a tiny bit from the end of loop and start of ending to blend)
    print("Applying crossfade...")
    final_audio = crossfade_arrays(segment_loop, segment_end, overlap_samples)

    # --- 3. NOISE REDUCTION ---
    print("Applying spectral gating (noise reduction)...")
    # stationary=True assumes the noise floor is constant (like a hum or hiss)
    # prop_decrease=0.1 is conservative to avoid artifacts
    clean_audio = nr.reduce_noise(
        y=final_audio, sr=sr, prop_decrease=0.1, stationary=True
    )

    # --- 4. EXPORT ---
    print(f"Saving to {output_file}...")
    sf.write(output_file, clean_audio, sr)
    print("Done.")


if __name__ == "__main__":
    process_audio()
