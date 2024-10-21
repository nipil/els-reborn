import dataclasses
import math

#############################################################################
# constants
#############################################################################

# defaults value taken from my HBM 330x600 lathe setup :
# https://www.usinages.com/threads/tour-hbm-330x600-cq6133-de-nipil.165426/
# of course you should adapt these to your setup !

# spindle encoder
SPINDLE_GEAR_TOOTH = 56
SPINDLE_OUTPUT_GEAR_TOOTH = 56
SPINDLE_OUTPUT_PULLEY_TOOTH = 40
SPINDLE_ENCODER_INPUT_PULLEY_TOOTH = 40
SPINDLE_ENCODER_PULSE_PER_REVOLUTION = 1000

# stepper
STEPPER_STEPS_PER_REV = 200
STEPPER_PHASE_POWER_SUPPLY_VOLTAGE = 60
STEPPER_NOMINAL_CURRENT_PER_PHASE_AMPERES = 6
STEPPER_PHASE_RESISTANCE_OHMS = 0.42
STEPPER_PHASE_INDUCTANCE_MILLIHENRY = 3.5
STEPPER_PHASE_INDUCTANCE_TOLERANCE_PERCENT = 0.2
STEPPER_PULLEY_TOOTH = 1
APRON_PULLEY_TOOTH = 1

# gearing in apron
#  the total *multiplied* reduction when engaging the longitudinal feed
#  (use 1 as numerator form worms and Z as denominator for wheels)
FEED_BED_GEAR_NUMERATOR = 1 * 40 * 36
FEED_BED_GEAR_DENOMINATOR = 36 * 56 * 60
#  the total *multiplied* reduction when engaging the cross feed
#  (use 1 as numerator form worms and Z as denominator for wheels)
FEED_CROSS_GEAR_DENOMINATOR = 1 * 40 * 56
FEED_CROSS_GEAR_NUMERATOR = 36 * 56 * 20

# rack-and-pinion output:
#    modulus of rack-and-pinion of bed linear motion output
FEED_BED_RACK_AND_PINION_MODULUS = 2
#    tooth count for bed output pinion gear (on rack-on-pinion)
FEED_BED_OUTPUT_PINION_TOOTH_COUNT = 14 

# screw outputs :
#   metric screws example :
#     3.5 mm pitch = 3.5 mm avdance (numerator) per 1 (denominator) revolutions
#     make it integers: 7 mm (numerator) per 2 (denominator) revolutions
#   imperial screws example:
#     11.5 TPI pitch = 25.4 mm advance (numerator) per 11.5 (denominator) revolutions
#     make it integers: 254 mm (numerator) per 115 (denominator) revolutions
LEAD_SCREW_PITCH_NUMERATOR = 3
LEAD_SCREW_PITCH_DENOMINATOR = 1
CROSS_SCREW_PITCH_NUMERATOR = 4
CROSS_SCREW_PITCH_DENOMINATOR = 1

@dataclasses.dataclass(order=True)
class ThreadSpec:
    _mm_per_rev: float = dataclasses.field(init=False, repr=False)
    mode: str
    designation: str
    advance_millimeters: int
    advance_revolutions: int

    def __post_init__(self):
        self._mm_per_rev = self.advance_millimeters / self.advance_revolutions

METRIC_PITCH_MM_PER_REV = (
    0.2,
    0.25,
    0.3,
    0.35,
    0.4,
    0.45,
    0.5,
    0.6,
    0.7,
    0.75,
    0.8,
    1,
    1.25,
    1.5,
    1.75,
    2,
    2.5,
    3,
    3.5,
    4,
    4.5,
    5,
    5.5,
    6
)

METRIC_THREADS = [
    ThreadSpec('M', f'{p}mm', int(p*100), int(100))
    for p in METRIC_PITCH_MM_PER_REV
]

IMPERIAL_PITCH_THREADS_PER_INCH = (
    2,
    3,
    4,
    4.5,
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    11.5,
    12,
    13,
    14,
    16,
    18,
    20,
    24,
    28,
    32,
    36,
    40,
    44,
    48,
    56,
    64,
    72,
    80,
    90,
    120,
    160
)

IMPERIAL_THREADS = [
    ThreadSpec('I', f'{p}tpi', int(25.4*10), int(p*10))
    for p in IMPERIAL_PITCH_THREADS_PER_INCH
]

THREADING_MODES = sorted(METRIC_THREADS+IMPERIAL_THREADS)

# see https://maker.pro/forums/resources/stepper-motor-max-rpm.54/
def max_stepper_rpm(steps_per_rev = None, phase_amps = None, phase_res = None, phase_mh = None, phase_volts = None):
    if steps_per_rev is None:
        steps_per_rev = STEPPER_STEPS_PER_REV
    if phase_amps is None:
        phase_amps = STEPPER_NOMINAL_CURRENT_PER_PHASE_AMPERES
    if phase_res is None:
        phase_res = STEPPER_PHASE_RESISTANCE_OHMS
    if phase_mh is None:
        phase_mh = STEPPER_PHASE_INDUCTANCE_MILLIHENRY
    if phase_volts is None:
        phase_volts = STEPPER_PHASE_POWER_SUPPLY_VOLTAGE
    return (60 / steps_per_rev) / (-((phase_mh / 1000) / phase_res) * math.log(1 - phase_amps * phase_res / phase_volts))

def characterize_stepper_rpm():
    stepper_max_rpm = max_stepper_rpm()
    print(f'{stepper_max_rpm=}')
    reducing_steps_increases_rpm = max_stepper_rpm(steps_per_rev = STEPPER_STEPS_PER_REV * 0.99) > stepper_max_rpm
    print(f'{reducing_steps_increases_rpm=}')
    reducing_amps_increases_rpm = max_stepper_rpm(phase_amps=STEPPER_NOMINAL_CURRENT_PER_PHASE_AMPERES * 0.99) > stepper_max_rpm
    print(f'{reducing_amps_increases_rpm=}')
    reducing_res_increases_rpm = max_stepper_rpm(phase_res=STEPPER_PHASE_RESISTANCE_OHMS * 0.99) > stepper_max_rpm
    print(f'{reducing_res_increases_rpm=}')
    reducing_mh_increases_rpm = max_stepper_rpm(phase_mh=STEPPER_PHASE_INDUCTANCE_MILLIHENRY * 0.99) > stepper_max_rpm
    print(f'{reducing_mh_increases_rpm=}')
    increasing_volts_increases_rpm = max_stepper_rpm(phase_volts=STEPPER_PHASE_POWER_SUPPLY_VOLTAGE * 1.01) > stepper_max_rpm
    print(f'{increasing_volts_increases_rpm=}')

def main():
    characterize_stepper_rpm()
    # for mode in THREADING_MODES:
    #     print(f'{mode._mm_per_rev:0>6.3f}', mode)

if __name__ == '__main__':
    main()
