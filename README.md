**1.**  **Experiment Setup using Holybro Telemetry Radio and HackRf One**


The specifications and features of the **Holybro Telemetry Radio** can be found [here](http://www.holybro.com/product/transceiver-telemetry-radio-v3/).

**HackRF One** is a popular software defined radio (SDR) device, supporting not only reception but also transmission of radio signals in the range between 1 MHz and 6 GHz.
For project status and information about HackRF hardware availability, visit the main [HackRF](https://greatscottgadgets.com/hackrf/) page at Great Scott Gadgets and the [Mossmann Github repository](https://github.com/mossmann/hackrf/wiki/Getting-Started-with-HackRF-and-GNU-Radio). 




|Holybro Telemetry Radio | HackRf One |
| ------------- | ------------- |
|<img src="uploads/81f6a5867216e0f486740f2c9ec537aa/holybro.PNG" alt="holybro" width="200"/>| <img src="uploads/492ccec079fe59ce1c55f9064fec5482/hackrf.PNG" alt="hackrf" width="200"/> |
|Holybro Telemetry Radio | HackRf One |
| ------------- | ------------- |
|<img src="uploads/81f6a5867216e0f486740f2c9ec537aa/holybro.PNG" alt="holybro" width="200"/>| <img src="uploads/492ccec079fe59ce1c55f9064fec5482/hackrf.PNG" alt="hackrf" width="200"/> |



* **1.1** **Serial Interface Settings**

**Experiment Setup**


|Experiment Setup|
| ------------- |
|<img src="uploads/13a76df96df50aec97fa69aec4f2b020/experiment_setup.jpg" width ="430"/>|


1.  installing the PuTTY software. [(putty for linux)](https://www.ssh.com/ssh/putty/linux)
2.  finding the serial usb port using this command in terminal on linux `cd /dev`
3.  for instance when the radio is connected to USB0 port, we can start putty with this configuration:

            `sudo putty /dev/ttyUSB0 -serial -sercfg 57600,8,n,1,N`
4.  this link [(mission planner)](https://ardupilot.org/copter/docs/common-3dr-radio-advanced-configuration-and-technical-information.html#common-3dr-radio-advanced-configuration-and-technical-information) explains quite well further configuration Options and about establishing the communication between the two radios.
5. The radios support a variant of the Hayes [‘AT’]( https://ardupilot.org/copter/docs/common-3dr-radio-advanced-configuration-and-technical-information.html#using-the-at-command-set)
 modem command set for configuration. Perhaps the most useful command is ‘ATI5’ which displays all user settable EEPROM parameters.
For instance we can enable/disable the [MAV link](https://en.wikipedia.org/wiki/MAVLink)  `ATs6=0` or `ATs6=1`.



* **1.2** **RF Signal Characteristics**

The following rf parameters are configured in both telemetry radios:
 
f_min=434MHz,

f_max=435MHz,
 
n_channels=1.

Since only one channel is used there is no frequency hopping. In order to visualize the spectrum of the transmitted signal, HackRf and  **osmocom spectrum analyser** can be used. 


* **1.3** **Recording the Transmitted Signal using the HackRf one and Universal Radio Hacker**

Universal Radio Hacker (URH) is an open source tool designed for protocol Analysis and implements a workflow such as interface for SDRs, intuitive demodulation or customised decodings. 

Necessary configuration of URH for recording :
*  Setting the Center frequency
*  Setting the gain
*  setting the sampling rate and bandwidth

The Frequency, Sample rate and Bandwidth are adjusted as the given table:

| Frequency | Sample rate | Bandwidth |
| ------------- | ------------- |---------|
| 434MHz| 2MSps |2MHz  | 

Since there are small guard bands at the beginning and the end of configured frequency range, we can set the center frequency to 434MHz.

<img src="uploads/b31c7505a61adba63eb4c511ded1b0c9/recording_settings.png" alt="record" width="400"/>
<p align="center">



The following images show the impact of increasing the receiver gain. The transmission happens with two different signal levels. When the receiver gain is low, the packets with high signal level can be demodulated correctly. Unfortunately the transmitted data could not be found while keeping the high signal level packets undistorted.

By increasing the receiver gain, packets with lower signal level appear between the periodic packets with high signal level, but the packets with high signal level are getting totally distorted. The packets with low signal level contain the transmitted data.  


 


<img src="uploads/a76790dc7b04c8882965d38cfa8e7cc3/gain_settings_annotated.png" alt="gain" width="700"/>




<img src="uploads/698bfa39799cfbb74cb9bc860007e67a/heavy_vs_not_heavy_annotated.png" alt="hevay_taffic" width="700"/>





**2.**  **Message Decoding**

* **2.1**  **URH parameters for demodulation**

  *  Samples/Symbol
  *  error tolerance
  *  center
  *  noise level

The first step before decoding is to set the URH parameters for correct demodulation.
By knowing the *air rate* value which is between *64000* and *64999* *Kbits/s* (the value is configured in the radio's) and since the sample rate **2*MSamples/s*** while we are recording the signal between the two telemetry radios, the value for the **samples/symbol** field in urh can be calculated as *sample rate/air rate* which is **31** with **1 bit error tolerance** .

$`2*10^6/64000=31.25`$

$`2*10^6/64999= 30.76`$

**Noise level**: the noise level should be set in a way that the gap between transmitted packets is interpreted as pause by urh demodulation. 
The following screenshot shows how to set the noise level.

<img src="uploads/01e32e3fcd2fa98f040c411afa8d0f41/untitled.png" alt="set_noise_level" width="500"/>











**Center**: The center value is determining the decision threshold between the two symbols which needs to be set quite carefully by checking both in demodulated view and the analogue signal.


<img src="uploads/9baa38910de31a55056744770c49da38/decision_threshold.png" alt="decision_thr" width="500"/>


The following image shows the FSK(GFSK) signal and the corresponding bits are highlighted in the sequence of demodulated bits.

<img src="uploads/96656494b9c1e53a1bd07d37127d3816/FSK_and_bits.png" alt="FSK_and_bits" width="500"/>


In the following image one bit is selected and one can see it is equivalent to 31 samples and the corresponding analogue signal.

<img src="uploads/eadf19549d616ef6dc1b9f103148f0ae/one_symbol.png" alt="one_symbol" width="500"/>




#### Telemetry Radio Block Diagram:

To understand the demodulated messages a closer look at the block diagram of the transmitting telemetry radios might be helpful.

 - TR is connected via Serial Port (UART) to the PC. ASCII messages are sent via the serial port to the telemetry radio.

 - TR is composed of a microcontroller and a RF-Transceiver module.
The microprocessor is preprocessing the data, e.g. adding MAVlink header, error correction, securing, buffering, generating heartbeat/status packets, reordering fields (MAVlink serialization).





<img src="uploads/05832e95b83a14c67450d8931cb39e17/untitled.png" alt="SERIAL_PORT" width="500"/>



**3.**  **Observations & protocol Analysis**


After setting of the parameters for a successful demodulation, we can start the analysis of the transmitted messages.


<img src="uploads/9382cd366c9bf9d2d2e8017e45c44711/protocol_analysis.png" alt="msg_296" width="500"/>

One can observe that the communication between these two telemetry radios is happening with two different signal strengths. We can assign two participants Alice and Bob to the high and low signal power correspondingly. In the following, we are ignoring the messages with high signal strengths, since the waveform is distorted due to the high receiver gain.
First step is to find preambles, synchronization and header messages.
The URH analysis function is a great tool for the protocol analysis.
 
**Decoding the data**

The telemetry radio is using data two different data encoding types:
ECC = 0, ECC = 1.

When the ECC is set to 1, golay encoding is used and the packet management is handled by the microcontroller.  
When the ECC is set to 0, the payload data is simply sent to the Si1000 module which takes care of forming the messages:
Every message has the same structure. It starts with a preamble (a series of 0s and 1s), followed by synchronization word, header, data and checksum.

| packet structure (automatic packet handler enabled)|packet structure (automatic packet handler disabled) |
| ------------- |----------- |
|<img src="uploads/6b3fccb37c288fbfd97ece8e16e03f57/packet_s_1.PNG" alt="packet_s_1" width="250"/>|  <img src="uploads/23aedcf98495f11081b3e48393ebcefe/packet_s_2.PNG" alt="packet_s_2" width="250"/>|

In the following, **ECC = 0**.


**Preamble: 01010101...01 (finishing with 1)**

**Sync word (2 bytes) : 0x2dd4**

**Header (2 bytes) : fixed length but variable content**.

**Data : variable length**

**CRC**

In order to align the messages, the following decoding setup in urh is applied to all messages.

**cut before : 010101010010110111010100**

<img src="uploads/80c9f4876c43c5852c0f5a45c6bd3815/decoding_align.png" alt="decision_thr" width="700"/>






Moreover the si1000 module also offers the possibility to whiten the data in order to avoid long repetitions of 0s or 1s.
If this feature is enabled, then at first the pseudo noise sequences used for whitening must be recovered.

The **PN sequences** for data whitening are generated as following:

**At transmitter** : data XOR PN9_sequences = transmitted_data

**At receiver** : transmitted_data XOR PN9_sequences = data.

In order to find the PN9 sequences, the data must be known. Therefore, the character "O" was continuously transmitted.


Once the PN9 sequences are known, they can be used to decode any transmitted messages.




The open source code for the telemetry radio can be found [here](https://github.com/ArduPilot/SiK)

Next step: using Telemetry radio and SDR for UAV detection.


   











































   











