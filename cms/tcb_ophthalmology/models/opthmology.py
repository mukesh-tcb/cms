
from odoo import api, fields, models ,_
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta


class TCBOphthalmologyEvaluation(models.Model):
    _name = "tcb.ophthalmology.evaluation"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Ophthalmology Evaluation"

    STATES = {'cancel': [('readonly', True)], 'done': [('readonly', True)]}

    name = fields.Char(string='Name', default='/', copy=False, tracking=True)
    patient_id = fields.Many2one('hms.patient', 'Patient', required=True, tracking=True)
    date = fields.Datetime('Date', default=fields.Datetime.now, help="Date of Consultation",tracking=True)
    age = fields.Char(compute="get_patient_age", string='Age', store=True,
            help="Computed patient age at the moment of the evaluation")
    physician_id = fields.Many2one('hms.physician', ondelete='restrict', string='Physician', 
        index=True, help='Physician\'s Name', tracking=True)
    appointment_id = fields.Many2one('hms.appointment', ondelete="restrict", 
        string='Appointment', tracking=True)
    diseases_ids = fields.Many2many("hms.diseases", 'hms_diseases_ophthalmology_rel', 'evaluation_id', 'diseases_id', "Disease", states=STATES)


    # Refraction Readings
    re_sph = fields.Float(string="Right Eye SPH")
    re_cyl = fields.Float(string="Right Eye CYL")
    re_axis = fields.Integer(string="Right Eye AXIS")
    re_add = fields.Float(string="Right Eye ADD")
    le_sph = fields.Float(string="Left Eye SPH")
    le_cyl = fields.Float(string="Left Eye CYL")
    le_axis = fields.Integer(string="Left Eye AXIS")
    le_add = fields.Float(string="Left Eye ADD")

    # Tonometer Readings
    nct_od = fields.Float(string="NCT OD")
    nct_os = fields.Float(string="NCT OS")
    gat_od = fields.Float(string="GAT OD")
    gat_os = fields.Float(string="GAT OS")
    cct_od = fields.Float(string="CCT OD")
    cct_os = fields.Float(string="CCT OS")

    # AR Readings - Dry and Wet
    ar_dry_re_sph = fields.Float(string="Dry SPH RE")
    ar_dry_re_cyl = fields.Float(string="Dry CYL RE")
    ar_dry_re_axis = fields.Integer(string="Dry AXIS RE")
    ar_dry_le_sph = fields.Float(string="Dry SPH LE")
    ar_dry_le_cyl = fields.Float(string="Dry CYL LE")
    ar_dry_le_axis = fields.Integer(string="Dry AXIS LE")

    # Examination
    color_vision = fields.Char(string="Color Vision")
    vision_od = fields.Float(string="Vision OD")
    vision_os = fields.Float(string="Vision OS")
    keratometry = fields.Char(string="Keratometry")

    # Additional Information Checkboxes
    workup_done = fields.Boolean(string="Workup Done")
    dilatation_needed = fields.Boolean(string="Dilatation Please")
    atropine_refraction = fields.Boolean(string="Atropine Refraction Please")
    cyclo_refraction = fields.Boolean(string="Cyclo Refraction Please")
    refraction_next_visit = fields.Boolean(string="Refraction Next Visit Please")

    # Notes
    optometrist_notes = fields.Text(string="Optometrist Notes")
    refraction_remarks = fields.Text(string="Refraction Remarks")
    
    
    
    
    
    #new fields for opthalmology
    eye_image = fields.Binary("Eye Image")
    unaided_re_dist_sph = fields.Float("RE Dist SPH")
    unaided_re_dist_cyl = fields.Float("RE Dist CYL")
    unaided_re_dist_axis = fields.Integer("RE Dist AXIS")
    unaided_re_dist_add = fields.Float("RE Dist ADD")
    unaided_re_near_sph = fields.Float("RE Near SPH")
    unaided_re_near_cyl = fields.Float("RE Near CYL")
    unaided_re_near_axis = fields.Integer("RE Near AXIS")
    unaided_re_near_add = fields.Float("RE Near ADD")
    
    unaided_le_dist_sph = fields.Float("LE Dist SPH")
    unaided_le_dist_cyl = fields.Float("LE Dist CYL")
    unaided_le_dist_axis = fields.Integer("LE Dist AXIS")
    unaided_le_dist_add = fields.Float("LE Dist ADD")
    unaided_le_near_sph = fields.Float("LE Near SPH")
    unaided_le_near_cyl = fields.Float("LE Near CYL")
    unaided_le_near_axis = fields.Integer("LE Near AXIS")
    unaided_le_near_add = fields.Float("LE Near ADD")
    
    # WITH PH fields
    ph_re_sph = fields.Float("PH RE SPH")
    ph_re_cyl = fields.Float("PH RE CYL")
    ph_re_axis = fields.Integer("PH RE AXIS")
    ph_re_add = fields.Float("PH RE ADD")
    ph_le_sph = fields.Float("PH LE SPH")
    ph_le_cyl = fields.Float("PH LE CYL")
    ph_le_axis = fields.Integer("PH LE AXIS")
    ph_le_add = fields.Float("PH LE ADD")
    
    # WITH EXISTING GLASS fields
    existing_re_dist_sph = fields.Float("Existing RE Dist SPH")
    existing_re_dist_cyl = fields.Float("Existing RE Dist CYL")
    existing_re_dist_axis = fields.Integer("Existing RE Dist AXIS")
    existing_re_dist_add = fields.Float("Existing RE Dist ADD")
    existing_re_near_sph = fields.Float("Existing RE Near SPH")
    existing_re_near_cyl = fields.Float("Existing RE Near CYL")
    existing_re_near_axis = fields.Integer("Existing RE Near AXIS")
    existing_re_near_add = fields.Float("Existing RE Near ADD")
    
    existing_le_dist_sph = fields.Float("Existing LE Dist SPH")
    existing_le_dist_cyl = fields.Float("Existing LE Dist CYL")
    existing_le_dist_axis = fields.Integer("Existing LE Dist AXIS")
    existing_le_dist_add = fields.Float("Existing LE Dist ADD")
    existing_le_near_sph = fields.Float("Existing LE Near SPH")
    existing_le_near_cyl = fields.Float("Existing LE Near CYL")
    existing_le_near_axis = fields.Integer("Existing LE Near AXIS")
    existing_le_near_add = fields.Float("Existing LE Near ADD")
    
    # AR Reading Status fields
    ar_dry_re_status = fields.Selection([
        ('normal', 'Normal'),
        ('abnormal', 'Abnormal')
    ], string="AR Dry RE Status")
    ar_dry_le_status = fields.Selection([
        ('normal', 'Normal'),
        ('abnormal', 'Abnormal')
    ], string="AR Dry LE Status")
    ar_wet_re_status = fields.Selection([
        ('normal', 'Normal'),
        ('abnormal', 'Abnormal')
    ], string="AR Wet RE Status")
    
    
    #bb ai 
    #keratometry fields
    
    keratometry_od_k1 = fields.Char(string="Keratometry OD K1")
    keratometry_od_k2 = fields.Char(string="Keratometry OD K2")
    keratometry_os_k1 = fields.Char(string="Keratometry OS K1")
    keratometry_os_k2 = fields.Char(string="Keratometry OS K2")
    
    #axis
    keratometry_od_k1_r1_axis = fields.Char(string="Keratometry OD K1 R1 Axis")
    keratometry_od_k2_r2_axis = fields.Char(string="Keratometry OD K2 R2 Axis")
    
    keratometry_os_k1_r1_axis = fields.Char(string="Keratometry OS K1 R1 Axis")
    keratometry_os_k2_r2_axis = fields.Char(string="Keratometry OS K2 R2 Axis")
    
    #AXL
    keratometry_od_k1_r1_axl = fields.Char(string="Keratometry OD K1 R1 Axl")
    keratometry_od_k2_r2_axl = fields.Char(string="Keratometry OD K2 R2 Axl")
    
    keratometry_os_k1_r1_axl = fields.Char(string="Keratometry OS K1 R1 Axl")
    keratometry_os_k2_r2_axl = fields.Char(string="Keratometry OS K2 R2 Axl")
    
    #PCIOL
    
    keratometry_od_k1_r1_pciol = fields.Char(string="Keratometry OD K1 R1 PCIOL")
    keratometry_od_k2_r2_pciol = fields.Char(string="Keratometry OD K2 R2 PCIOL")
    
    keratometry_os_k1_r1_pciol = fields.Char(string="Keratometry OS K1 R1 PCIOL")
    keratometry_os_k2_r2_pciol = fields.Char(string="Keratometry OS K2 R2 PCIOL")
    
    #R1 R2
    keratometry_od_k1_r1 = fields.Char(string="Keratometry OD K1 R1")
    keratometry_od_k2_r2 = fields.Char(string="Keratometry OD K2 R2")
    

    keratometry_os_k1_r1 = fields.Char(string="Keratometry OS K1 R1")
    keratometry_os_k2_r2 = fields.Char(string="Keratometry OS K2 R2")

    
    
    
    color_vision_od = fields.Float(string="Color Vision OD")
    color_vision_os = fields.Float(string="Color Vision OS")
    
    tonometry_od_nct = fields.Float(string="Tonometry NCT OD")    
    tonometry_os_nct = fields.Float(string="Tonometry NCT OS")
    
    tonometry_od_gat = fields.Float(string="Tonometry GAT OD")    
    tonometry_os_gat = fields.Float(string="Tonometry GAT OS")
    
    tonometry_od_cct = fields.Float(string="Tonometry CCT OD")    
    tonometry_os_cct = fields.Float(string="Tonometry CCT OS")

    nct_machine_od = fields.Float(string="Net Machine OD")
    nct_machine_os = fields.Float(string="Net Machine OS")

    prism_value_re = fields.Float(string="Prism Value RE")
    prism_value_le = fields.Float(string="Prism Value LE")
    
    pachy_re = fields.Char(string='Pachy RE')
    pachy_le = fields.Char(string='Pachy LE')
    
    
    
    # DRY AR READINGS
    ar_dry_sph_right = fields.Many2one("eye.sph", string="AR DRY SPH Right")
    ar_dry_cyl_right = fields.Many2one("eye.cyl", string="AR DRY CYL Right")
    ar_dry_axis_right = fields.Many2one("eye.axis", string="AR DRY AXIS Right")
    ar_dry_status_right = fields.Selection(
        [('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'),
        ('e', 'E')], string="AR DRY STATUS Right")
    ar_dry_sph_left = fields.Many2one("eye.sph", string="AR DRY SPH Left")
    ar_dry_cyl_left = fields.Many2one("eye.cyl", string="AR DRY CYL Left")
    ar_dry_axis_left = fields.Many2one("eye.axis", string="AR DRY AXIS Left")
    ar_dry_status_left = fields.Selection(
        [('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'),
        ('e', 'E')], string="AR DRY STATUS Left")
    
    ar_wet_sph_right = fields.Many2one("eye.sph", string="AR WET SPH Right")
    ar_wet_cyl_right = fields.Many2one("eye.cyl", string="AR WET CYL Right")
    ar_wet_axis_right = fields.Many2one("eye.axis", string="AR WET AXIS Right")
    ar_wet_status_right = fields.Selection(
        [('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'),
        ('e', 'E')], string="AR WET STATUS Right")
    ar_wet_sph_left = fields.Many2one("eye.sph", string="AR WET SPH Left")
    ar_wet_cyl_left = fields.Many2one("eye.cyl", string="AR WET CYL Left")
    ar_wet_axis_left = fields.Many2one("eye.axis", string="AR WET AXIS Left")
    ar_wet_status_left = fields.Selection(
        [('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'),
        ('e', 'E')], string="AR WET STATUS Left")


# POG1 for refrection readings page 
    pog1_ref_sph_re = fields.Many2one("eye.sph", string="SPH POG1 RE")
    pog1_ref_cyl_re = fields.Many2one("eye.cyl", string="CYL POG1 RE")
    pog1_ref_axis_re = fields.Many2one("eye.axis", string="AXIS POG1 RE")
    pog1_ref_add_re = fields.Many2one("eye.add", string="ADD POG1 RE")

    pog1_ref_sph_le = fields.Many2one("eye.sph", string="SPH POG1 LE")
    pog1_ref_cyl_le = fields.Many2one("eye.cyl", string="CYL POG1 LE")
    pog1_ref_axis_le = fields.Many2one("eye.axis", string="AXIS POG1 LE")
    pog1_ref_add_le = fields.Many2one("eye.add", string="ADD POG1 LE")
    pog1_ref_type = fields.Selection([('normal', 'Normal'), ('abnormal', 'Abnormal')], string="POG1 Type")
    pog1_ref_how_old_value = fields.Char(string="How Old")
    pog1_ref_how_old_select = fields.Selection([('year', 'Year'), ('years', 'Years'), ('month', 'Month'),
                                                    ('months', 'Months'), ('week', 'Week'), ('weeks', 'Weeks'),
                                                    ('day', 'Day'),
                                                    ('days', 'Days')], string="How Old Type")
    pog1_ref_done_by = fields.Char(string="Done By")

    # POG2 for refrection readings page 
    pog2_ref_sph_re = fields.Many2one("eye.sph", string="SPH RE")
    pog2_ref_cyl_re = fields.Many2one("eye.cyl", string="CYL RE")
    pog2_ref_axis_re = fields.Many2one("eye.axis", string="AXIS RE")
    pog2_ref_add_re = fields.Many2one("eye.add", string="ADD RE")

    pog2_ref_sph_le = fields.Many2one("eye.sph", string="SPH LE")
    pog2_ref_cyl_le = fields.Many2one("eye.cyl", string="CYL LE")
    pog2_ref_axis_le = fields.Many2one("eye.axis", string="AXIS LE")
    pog2_ref_add_le = fields.Many2one("eye.add", string="ADD LE")
    pog2_ref_type = fields.Selection([('normal', 'Normal'), ('abnormal', 'Abnormal')], string="POG Type")
    pog2_ref_how_old_value = fields.Char(string="How Old")
    pog2_ref_how_old_select = fields.Selection([('year', 'Year'), ('years', 'Years'), ('month', 'Month'),
                                                    ('months', 'Months'), ('week', 'Week'), ('weeks', 'Weeks'),
                                                    ('day', 'Day'),
                                                    ('days', 'Days')], string="How Old Type")
    pog2_ref_done_by = fields.Char(string="Done By")

    # Refraction
    refraction_ipd = fields.Char(string="IPD")
    # Dist
    re_dist_va = fields.Many2one("unaided.dist.eye", "RE Dist. VA")
    refraction_dist_sph_re = fields.Many2one("eye.sph", string="SPH RE")
    refraction_dist_cyl_re = fields.Many2one("eye.cyl", string="CYL RE")
    refraction_dist_axis_re = fields.Many2one("eye.axis", string="AXIS RE")

    refraction_dist_sph_le = fields.Many2one("eye.sph", string="SPH LE")
    refraction_dist_cyl_le = fields.Many2one("eye.cyl", string="CYL LE")
    refraction_dist_axis_le = fields.Many2one("eye.axis", string="AXIS LE")
    le_dist_va = fields.Many2one("unaided.dist.eye", "LE Dist. VA")

    # Near
    re_near_va = fields.Many2one("unaided.near.eye", "RE Dist. VA")
    refraction_near_sph_re = fields.Many2one("eye.sph", string="SPH RE")
    refraction_near_cyl_re = fields.Many2one("eye.cyl", string="CYL RE")
    refraction_near_axis_re = fields.Many2one("eye.axis", string="AXIS RE")

    refraction_near_sph_le = fields.Many2one("eye.sph", string="SPH LE")
    refraction_near_cyl_le = fields.Many2one("eye.cyl", string="CYL LE")
    refraction_near_axis_le = fields.Many2one("eye.axis", string="AXIS LE")
    le_near_va = fields.Many2one("unaided.near.eye", "LE Dist. VA")


    # Last
    # Dist
    re_dist_va_last = fields.Many2one("unaided.dist.eye", "RE Dist. VA")
    refraction_dist_sph_re_last = fields.Many2one("eye.sph", string="SPH RE")
    refraction_dist_cyl_re_last = fields.Many2one("eye.cyl", string="CYL RE")
    refraction_dist_axis_re_last = fields.Many2one("eye.axis", string="AXIS RE")

    refraction_dist_sph_le_last = fields.Many2one("eye.sph", string="SPH LE")
    refraction_dist_cyl_le_last = fields.Many2one("eye.cyl", string="CYL LE")
    refraction_dist_axis_le_last = fields.Many2one("eye.axis", string="AXIS LE")
    le_dist_va_last = fields.Many2one("unaided.dist.eye", "LE Dist. VA")

    # Near
    re_near_va_last = fields.Many2one("unaided.near.eye", "RE Dist. VA")
    refraction_near_sph_re_last = fields.Many2one("eye.sph", string="SPH RE")
    refraction_near_cyl_re_last = fields.Many2one("eye.cyl", string="CYL RE")
    refraction_near_axis_re_last = fields.Many2one("eye.axis", string="AXIS RE")

    refraction_near_sph_le_last = fields.Many2one("eye.sph", string="SPH LE")
    refraction_near_cyl_le_last = fields.Many2one("eye.cyl", string="CYL LE")
    refraction_near_axis_le_last = fields.Many2one("eye.axis", string="AXIS LE")
    le_near_va_last = fields.Many2one("unaided.near.eye", "LE Dist. VA")

    # Prism Values
    prism_value_re = fields.Char(string="Prism Value RE")
    prism_value_le = fields.Char(string="Prism Value LE")

    # Notes
    
    
    ref_workup_done = fields.Boolean(string="Workup Done")
    ref_wet_ar_please = fields.Boolean(string="Wet AR Please")
    ref_dilation_please = fields.Boolean(string="Dilation Please")
    ref_pmt_please = fields.Boolean(string="PMT Please")
    cyclo_refraction_please = fields.Boolean(string="Cyclo Refraction Please")
    atropine_refraction_please = fields.Boolean(string="Atropine Refraction Please")
    refraction_next_visit_please = fields.Boolean(string="Refraction Next Visit Please")

##for presenting comlaints -- 

    DURATION_SELECTION = [
        ('d', 'Days'),
        ('m', 'Months'),
        ('y', 'Years'),
        ('h', 'Hours'),
        ('min', 'Minutes')
    ]

    EYE_SELECTION = [
        ('re', 'RE'),
        ('le', 'LE'),
        ('be', 'BE')
    ]

    # Symptoms fields
    watering = fields.Boolean(string="Watering in")
    watering_eye = fields.Selection(EYE_SELECTION, string="Watering Eye")
    watering_since = fields.Char(string="Watering Since")
    watering_duration_type = fields.Selection(DURATION_SELECTION, string="Watering Duration Type")

    redness = fields.Boolean(string="Redness in")
    redness_eye = fields.Selection(EYE_SELECTION, string="Redness Eye")
    redness_since = fields.Char(string="Redness Since")
    redness_duration_type = fields.Selection(DURATION_SELECTION, string="Redness Duration Type")

    decreased_vision = fields.Boolean(string="Decreased vision")
    decreased_vision_eye = fields.Selection(EYE_SELECTION, string="Decreased Vision Eye")
    decreased_vision_since = fields.Char(string="Decreased Vision Since")
    decreased_vision_duration_type = fields.Selection(DURATION_SELECTION, string="Decreased Vision Duration Type")

    pain = fields.Boolean(string="Pain")
    pain_eye = fields.Selection(EYE_SELECTION, string="Pain Eye")
    pain_since = fields.Char(string="Pain Since")
    pain_duration_type = fields.Selection(DURATION_SELECTION, string="Pain Duration Type")

    discharge = fields.Boolean(string="Discharge")
    discharge_eye = fields.Selection(EYE_SELECTION, string="Discharge Eye")
    discharge_since = fields.Char(string="Discharge Since")
    discharge_duration_type = fields.Selection(DURATION_SELECTION, string="Discharge Duration Type")

    itching = fields.Boolean(string="Itching")
    itching_eye = fields.Selection(EYE_SELECTION, string="Itching Eye")
    itching_since = fields.Char(string="Itching Since")
    itching_duration_type = fields.Selection(DURATION_SELECTION, string="Itching Duration Type")

    burning = fields.Boolean(string="Burning")
    burning_eye = fields.Selection(EYE_SELECTION, string="Burning Eye")
    burning_since = fields.Char(string="Burning Since")
    burning_duration_type = fields.Selection(DURATION_SELECTION, string="Burning Duration Type")

    swelling = fields.Boolean(string="Swelling")
    swelling_eye = fields.Selection(EYE_SELECTION, string="Swelling Eye")
    swelling_since = fields.Char(string="Swelling Since")
    swelling_duration_type = fields.Selection(DURATION_SELECTION, string="Swelling Duration Type")

    irritation = fields.Boolean(string="Irritation")
    irritation_eye = fields.Selection(EYE_SELECTION, string="Irritation Eye")
    irritation_since = fields.Char(string="Irritation Since")
    irritation_duration_type = fields.Selection(DURATION_SELECTION, string="Irritation Duration Type")

    foreign_body = fields.Boolean(string="Foreign body")
    foreign_body_eye = fields.Selection(EYE_SELECTION, string="Foreign Body Eye")
    foreign_body_since = fields.Char(string="Foreign Body Since")
    foreign_body_duration_type = fields.Selection(DURATION_SELECTION, string="Foreign Body Duration Type")

    other = fields.Boolean(string="Other")
    other_eye = fields.Selection(EYE_SELECTION, string="Other Eye")
    other_since = fields.Char(string="Other Since")
    other_duration_type = fields.Selection(DURATION_SELECTION, string="Other Duration Type")
    other_description = fields.Char(string="Other Description")