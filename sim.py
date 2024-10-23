import dataclasses
import fractions
import math

#############################################################################
# constants
#############################################################################

# Fractional definition for PI, to avoir floating point calculations
# approx. error : 0.8µm over 10 meters, for a 14-tooth mod-2 rack & pinion
PI_NUMERATOR = 355
PI_DENOMINATOR = 113

# defaults value taken from my HBM 330x600 lathe setup :
# https://www.usinages.com/threads/tour-hbm-330x600-cq6133-de-nipil.165426/
# of course you should adapt these to your setup !

# spindle encoder
SPINDLE_GEAR_DRIVER = 56
SPINDLE_OUTPUT_GEAR_DRIVEN = 56
SPINDLE_OUTPUT_PULLEY_DRIVER = 40
SPINDLE_ENCODER_PULLEY_DRIVEN = 40
SPINDLE_ENCODER_PULSE_PER_REVOLUTION = 1000

# stepper motor
STEPPER_STEPS_PER_REV = 200
STEPPER_PULLEY_DRIVER = 1
APRON_PULLEY_DRIVEN = 1

# stepper electrical
STEPPER_PHASE_POWER_SUPPLY_VOLTAGE = 60
STEPPER_NOMINAL_CURRENT_PER_PHASE_AMPERES = 6
STEPPER_PHASE_RESISTANCE_OHMS = 0.42
STEPPER_PHASE_INDUCTANCE_MILLIHENRY = 3.5
STEPPER_PHASE_INDUCTANCE_TOLERANCE_PERCENT = 0.2

## Threading mode

# screw outputs :
#   metric screws example :
#     3.5 mm pitch = 3.5 mm avdance (numerator) per 1 (denominator) revolutions
#     make it integers: 7 mm (numerator) per 2 (denominator) revolutions
#   imperial screws example:
#     11.5 TPI pitch = 25.4 mm advance (numerator) per 11.5 (denominator) revolutions
#     make it integers: 254 mm (numerator) per 115 (denominator) revolutions
APRON_SHAFT_DRIVER = 1
LEAD_SCREW_DRIVEN = 1
LEAD_SCREW_PITCH_NUMERATOR = 3
LEAD_SCREW_PITCH_DENOMINATOR = 1

## Turning mode

# gearing in apron
#  the total *multiplied* reduction when engaging the longitudinal feed
#  (use 1 as numerator form worms and Z as denominator for wheels)
APRON_BED_GEAR_DRIVER = 1 * 40 * 36
APRON_BED_GEAR_DRIVEN = 36 * 56 * 60
# rack-and-pinion output:
#    modulus of rack-and-pinion of bed linear motion output
APRON_BED_PINION_MODULUS = 2
#    tooth count for bed output pinion gear (on rack-on-pinion)
APRON_BED_PINION_DRIVER = 14 

## Facing mode

#  the total *multiplied* reduction when engaging the cross feed
#  (use 1 as numerator form worms and Z as denominator for wheels)
APRON_CROSS_GEAR_DRIVER = 1 * 40 * 56
APRON_CROSS_GEAR_DRIVEN = 36 * 56 * 20

# screw outputs :
#   metric screws example :
#     3.5 mm pitch = 3.5 mm avdance (numerator) per 1 (denominator) revolutions
#     make it integers: 7 mm (numerator) per 2 (denominator) revolutions
#   imperial screws example:
#     11.5 TPI pitch = 25.4 mm advance (numerator) per 11.5 (denominator) revolutions
#     make it integers: 254 mm (numerator) per 115 (denominator) revolutions
CROSS_SCREW_PITCH_NUMERATOR = 4
CROSS_SCREW_PITCH_DENOMINATOR = 1


@dataclasses.dataclass(order=True)
class Advance:
    _mm_per_rev: float = dataclasses.field(init=False, repr=False)
    mode: str
    designation: str
    advance_numerator_millimeters: int
    advance_denominator_revolutions: int

    def __post_init__(self):
        self._mm_per_rev = self.advance_numerator_millimeters / self.advance_denominator_revolutions

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
    Advance('M', f'{p}mm/t', int(p*100), 100)
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
    Advance('I', f'{p}tpi', int(25.4*10), int(p*10))
    for p in IMPERIAL_PITCH_THREADS_PER_INCH
]

THREADING_MODES = sorted(METRIC_THREADS + IMPERIAL_THREADS)

METRIC_FEED_MM_PER_REV = (
    0.005,
    0.01,
    0.015,
    0.02,
    0.03,
    0.04,
    0.05,
    0.06,
    0.08,
    0.1,
    0.12,
    0.15,
    0.2,
    0.25,
    0.3,
    0.4,
    0.5,
    0.6,
    0.75,
    1,
    1.25,
    1.5,
    1.75,
    2
)

METRIC_FEEDS = [
    Advance('M', f'{p}mm/t', int(p*1000), 1000)
    for p in METRIC_FEED_MM_PER_REV
]

IMPERIAL_FEED_THOU_PER_REV = (
    0.2,
    0.5,
    1,
    1.5,
    2,
    2.5,
    3,
    3.5,
    4,
    5,
    6,
    8,
    10,
    12,
    16,
    20,
    25,
    30,
    40,
    50,
    60,
    70,
    80
)

IMPERIAL_FEEDS = [
    Advance('I', f'{p}th/r', int(p*10*25.4*10), 10*1000*10)
    for p in IMPERIAL_FEED_THOU_PER_REV
]

FEED_MODES = sorted(METRIC_FEEDS + IMPERIAL_FEEDS)

SPINDLE_RPM = (
    65,
    100,
    115,
    170,
    200,
    300,
    350,
    520,
    600,
    900,
    1050,
    1600
)

#############################################################################
# solving for K (a.k.a. how many stepper steps per spindle encoder pulse)
#############################################################################
# 
### Spindle to apron
# 
# spindle_revolutions * SPINDLE_GEAR_DRIVER / SPINDLE_OUTPUT_GEAR_DRIVEN
# = spindle_output_revolutions
# 
# spindle_output_revolutions * SPINDLE_OUTPUT_PULLEY_DRIVER / SPINDLE_ENCODER_PULLEY_DRIVEN
# = spindle_encoder_revolutions
#
# spindle_encoder_revolutions * SPINDLE_ENCODER_PULSE_PER_REVOLUTION
# = spindle_encoder_pulses
#
# spindle_encoder_pulses * K
# = stepper_motor_steps
#
# stepper_motor_steps / STEPPER_STEPS_PER_REV
# = stepper_motor_revolutions
#
# stepper_motor_revolutions * STEPPER_PULLEY_DRIVER / APRON_PULLEY_DRIVEN
# = apron_input_revolutions
#
### Threading mode
#
# apron_input_revolutions * APRON_SHAFT_DRIVER / LEAD_SCREW_DRIVEN
# = lead_screw_revolutions
#
# lead_screw_revolutions * LEAD_SCREW_PITCH_NUMERATOR / LEAD_SCREW_PITCH_DENOMINATOR
# = lead_screw_advance_per_revolution
#
### Facing mode
#
# apron_input_revolutions * APRON_CROSS_GEAR_DRIVER / APRON_CROSS_GEAR_DRIVEN
# = cross_screw_revolutions
#
# cross_screw_revolutions * CROSS_SCREW_PITCH_NUMERATOR / CROSS_SCREW_PITCH_DENOMINATOR
# = cross_screw_advance_per_revolution
#
### Turning mode
#
# apron_input_revolutions * APRON_BED_GEAR_DRIVER / APRON_BED_GEAR_DRIVEN
# = bed_pinion_revolutions
#
# bed_pinion_revolutions * APRON_BED_PINION_MODULUS * APRON_BED_PINION_DRIVER * PI
# = bed_pinion_advance_per_revolution

### Solutions for K (K unit is stepper_steps per encoder_pulse)
#
# K_threading = lead_screw_advance_per_revolution * (
#   APRON_PULLEY_DRIVEN *
#   LEAD_SCREW_DRIVEN *
#   LEAD_SCREW_PITCH_DENOMINATOR *
#   SPINDLE_ENCODER_PULLEY_DRIVEN *
#   SPINDLE_OUTPUT_GEAR_DRIVEN *
#   STEPPER_STEPS_PER_REV
# ) / (
#   APRON_SHAFT_DRIVER *
#   LEAD_SCREW_PITCH_NUMERATOR *
#   SPINDLE_ENCODER_PULSE_PER_REVOLUTION *
#   SPINDLE_GEAR_DRIVER *
#   SPINDLE_OUTPUT_PULLEY_DRIVER *
#   STEPPER_PULLEY_DRIVER *
#   spindle_revolutions
# )
def K_threading(lead_screw_advance_per_revolution: Advance):
    numerator = lead_screw_advance_per_revolution.advance_numerator_millimeters * (
        APRON_PULLEY_DRIVEN *
        LEAD_SCREW_DRIVEN *
        LEAD_SCREW_PITCH_DENOMINATOR *
        SPINDLE_ENCODER_PULLEY_DRIVEN *
        SPINDLE_OUTPUT_GEAR_DRIVEN *
        STEPPER_STEPS_PER_REV
    )
    denominator = lead_screw_advance_per_revolution.advance_denominator_revolutions* (
        APRON_SHAFT_DRIVER *
        LEAD_SCREW_PITCH_NUMERATOR *
        SPINDLE_ENCODER_PULSE_PER_REVOLUTION *
        SPINDLE_GEAR_DRIVER *
        SPINDLE_OUTPUT_PULLEY_DRIVER *
        STEPPER_PULLEY_DRIVER
        # per 1 spindle revolution
    )
    return numerator, denominator, fractions.Fraction(numerator, denominator)

# K_facing = cross_screw_advance_per_revolution * (
#   APRON_CROSS_GEAR_DRIVEN *
#   APRON_PULLEY_DRIVEN *
#   CROSS_SCREW_PITCH_DENOMINATOR *
#   SPINDLE_ENCODER_PULLEY_DRIVEN *
#   SPINDLE_OUTPUT_GEAR_DRIVEN *
#   STEPPER_STEPS_PER_REV
# ) / (
#   APRON_CROSS_GEAR_DRIVER *
#   CROSS_SCREW_PITCH_NUMERATOR *
#   SPINDLE_ENCODER_PULSE_PER_REVOLUTION *
#   SPINDLE_GEAR_DRIVER *
#   SPINDLE_OUTPUT_PULLEY_DRIVER *
#   STEPPER_PULLEY_DRIVER *
#   spindle_revolutions
# )
def K_facing(cross_screw_advance_per_revolution: Advance):
    numerator = cross_screw_advance_per_revolution.advance_numerator_millimeters * (
        APRON_CROSS_GEAR_DRIVEN *
        APRON_PULLEY_DRIVEN *
        CROSS_SCREW_PITCH_DENOMINATOR *
        SPINDLE_ENCODER_PULLEY_DRIVEN *
        SPINDLE_OUTPUT_GEAR_DRIVEN *
        STEPPER_STEPS_PER_REV
    )
    denominator = cross_screw_advance_per_revolution.advance_denominator_revolutions * (
        APRON_CROSS_GEAR_DRIVER *
        CROSS_SCREW_PITCH_NUMERATOR *
        SPINDLE_ENCODER_PULSE_PER_REVOLUTION *
        SPINDLE_GEAR_DRIVER *
        SPINDLE_OUTPUT_PULLEY_DRIVER *
        STEPPER_PULLEY_DRIVER
        # per 1 spindle revolution
    )
    return numerator, denominator, fractions.Fraction(numerator, denominator)

# K_turning = bed_pinion_advance_per_revolution * (
#   APRON_BED_GEAR_DRIVEN *
#   APRON_PULLEY_DRIVEN *
#   SPINDLE_ENCODER_PULLEY_DRIVEN *
#   SPINDLE_OUTPUT_GEAR_DRIVEN *
#   STEPPER_STEPS_PER_REV
# ) / (
#   APRON_BED_GEAR_DRIVER *
#   APRON_BED_PINION_DRIVER *
#   APRON_BED_PINION_MODULUS *
#   PI *
#   SPINDLE_ENCODER_PULSE_PER_REVOLUTION *
#   SPINDLE_GEAR_DRIVER *
#   SPINDLE_OUTPUT_PULLEY_DRIVER *
#   STEPPER_PULLEY_DRIVER *
#   spindle_revolutions
# )
def K_turning(bed_pinion_advance_per_revolution: Advance):
    numerator = bed_pinion_advance_per_revolution.advance_numerator_millimeters * (
        APRON_BED_GEAR_DRIVEN *
        APRON_PULLEY_DRIVEN *
        SPINDLE_ENCODER_PULLEY_DRIVEN *
        SPINDLE_OUTPUT_GEAR_DRIVEN *
        STEPPER_STEPS_PER_REV *
        PI_DENOMINATOR
    )
    denominator = bed_pinion_advance_per_revolution.advance_denominator_revolutions * (
        PI_NUMERATOR *
        APRON_BED_GEAR_DRIVER *
        APRON_BED_PINION_DRIVER *
        APRON_BED_PINION_MODULUS *
        SPINDLE_ENCODER_PULSE_PER_REVOLUTION *
        SPINDLE_GEAR_DRIVER *
        SPINDLE_OUTPUT_PULLEY_DRIVER *
        STEPPER_PULLEY_DRIVER
        # per 1 spindle revolution
    )
    return numerator, denominator, fractions.Fraction(numerator, denominator)

#############################################################################
# utilities
#############################################################################

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
    print('Threading')
    for mode in THREADING_MODES:
        print(f'{mode._mm_per_rev:0>6.3f}', mode)
    print('Feeding')
    for mode in FEED_MODES:
        print(f'{mode._mm_per_rev:0>6.3f}', mode)

if __name__ == '__main__':
    main()
