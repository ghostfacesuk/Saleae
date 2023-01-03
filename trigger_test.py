#from saleae import automation
import os
import os.path
from datetime import datetime
from saleae.automation import *

## Connect to the running Logic 2 Application on port `10430`.
## Alternatively you can use automation.Manager.launch() to launch a new Logic 2 process - see
## the API documentation for more details.
## Using the `with` statement will automatically call manager.close() when exiting the scope. If you
## want to use `automation.Manager` outside of a `with` block, you will need to call `manager.close()` manually.
with Manager.connect(port=10430) as manager:

    ## Configure the capturing device to record on digital channels 0, 1, 2, and 3,
    ## with a sampling rate of 10 MSa/s, and a logic level of 3.3V.
    ## The settings chosen here will depend on your device's capabilities and what
    ## you can configure in the Logic 2 UI.
    device_configuration = LogicDeviceConfiguration(
    #    enabled_digital_channels=[0, 1, 2, 3],
        enabled_digital_channels=[0, 4, 6],
        digital_sample_rate=16_000_000,
    #    digital_threshold_volts=1.0,
    )

    ## Looking for falling edge on Channel 4 and then record for 10s
    capture_configuration = CaptureConfiguration(
        # capture_mode=automation.TimedCaptureMode(duration_seconds=5.0)
        capture_mode=DigitalTriggerCaptureMode(
            trigger_type=DigitalTriggerType.FALLING,
            trigger_channel_index=4,
            trim_data_seconds=10.0,
            after_trigger_seconds=10.0,
            min_pulse_width_seconds=None,
            max_pulse_width_seconds=None,
            )
    )

    ## Start a capture - the capture will be automatically closed when leaving the `with` block
    ## Note: The serial number 'F4241' is for the Logic Pro 16 demo device.
    ##       To use a real device, you can:
    ##         1. Omit the `device_id` argument. Logic 2 will choose the first real (non-simulated) device.
    ##         2. Use the serial number for your device. See the "Finding the Serial Number
    ##            of a Device" section for information on finding your device's serial number.
    with manager.start_capture(
    #        device_id='F4241',
            device_id='DDF169A30AB7B91A',
            device_configuration=device_configuration,
            capture_configuration=capture_configuration) as capture:

        print("\nTest started...")

        ## Wait until the capture has finished
        ## This will take about 5 seconds because we are using a timed capture mode
        capture.wait()

        ## Add an analyzer to the capture
        ## Note: The simulator output is not actual SPI data

        #spi_analyzer = capture.add_analyzer('SPI', label=f'Test Analyzer', settings={
        #    'MISO': 0,
        #    'Clock': 1,
        #    'Enable': 2,
        #    'Bits per Transfer': '8 Bits per Transfer (Standard)'
        #})

        ## Store output in a timestamped directory
        output_dir = os.path.join(os.getcwd(), f'C:\Output Files\output-{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}')
        os.makedirs(output_dir)

        print("\nTest complete, exporting files...")

        ## Export analyzer data to a CSV file
        #analyzer_export_filepath = os.path.join(output_dir, 'spi_export.csv')
        #capture.export_data_table(
        #    filepath=analyzer_export_filepath,
        #    analyzers=[spi_analyzer]
        #)

        ## Export raw digital data to a CSV file
        capture.export_raw_data_csv(directory=output_dir, digital_channels=[1, 4, 7])

        ## Finally, save the capture to a file
        capture_filepath = os.path.join(output_dir, 'Trigger_Capture.sal')
        capture.save_capture(filepath=capture_filepath)

        print(f"\nExport complete, files can be found in...\n{output_dir}")