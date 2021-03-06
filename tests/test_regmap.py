#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Register map module tests.
"""

import pytest
from corsair import BitField, Register, RegisterMap
from corsair import Configuration
import copy


class TestBitField:
    """Class 'Bitfield' testing."""
    def test_create(self):
        """Test of a bit field creation."""
        name = 'bf_a'
        description = ''
        initial = 0
        width = 1
        lsb = 0
        access = 'rw'
        modifiers = []
        bf = BitField(name)
        print(repr(bf))
        print(bf)
        assert ((name, description, initial, width, lsb, access, modifiers) ==
                (bf.name, bf.description, bf.initial, bf.width, bf.lsb, bf.access, bf.modifiers))

    def test_eq(self):
        """Test of equality comparision of bit fields."""
        bf1 = BitField('bf_a', initial=2)
        bf2 = copy.deepcopy(bf1)
        assert bf1 == bf2

    def test_ne(self):
        """Test of non equality comparision of bit fields."""
        bf1 = BitField('bf_a', initial=2)
        bf2 = copy.deepcopy(bf1)
        bf2 .initial = 3
        assert bf1 != bf2

    def test_initial_access(self):
        """Test of accessing to 'initial' attribute of a bit field."""
        bf = BitField('bf_a')
        bf.initial = 2
        assert bf.initial == 2

    def test_initial_init_wrong(self):
        """Test of initializing a bit field with a wrong 'initial' value."""
        with pytest.raises(ValueError):
            BitField('bf_a', initial=0.0)

    def test_initial_set_wrong(self):
        """Test of setting wrong value to 'initial' attribute of a bit field."""
        bf = BitField('bf_a')
        with pytest.raises(ValueError):
            bf.initial = 0.0

    def test_width_access(self):
        """Test of accessing to 'width' attribute of a bit field."""
        bf = BitField('bf_a')
        bf.width = 16
        assert bf.width == 16

    def test_width_init_wrong(self):
        """Test of initializing a bit field with a wrong 'width' value."""
        with pytest.raises(ValueError):
            BitField('bf_a', width='0')

    def test_width_set_wrong(self):
        """Test of setting wrong value to 'width' attribute of a bit field."""
        bf = BitField('bf_a')
        with pytest.raises(ValueError):
            bf.width = 0

    def test_lsb_access(self):
        """Test of accessing to 'lsb' attribute of a bit field."""
        bf = BitField('bf_a')
        bf.lsb = 3
        assert bf.lsb == 3

    def test_lsb_init_wrong(self):
        """Test of initializing a bit field with a wrong 'lsb' value."""
        with pytest.raises(ValueError):
            BitField('bf_a', lsb='3')

    def test_lsb_set_wrong(self):
        """Test of setting wrong value to 'lsb' attribute of a bit field."""
        bf = BitField('bf_a')
        with pytest.raises(ValueError):
            bf.lsb = -1

    def test_msb_access(self):
        """Test of accessing to 'msb' attribute of a bit field."""
        bf = BitField('bf_a', lsb=2, width=4)
        assert bf.msb == 5

    def test_access_access(self):
        """Test of accessing to 'access' attribute of a bit field."""
        bf = BitField('bf_a')
        bf.access = 'wo'
        assert bf.access == 'wo'

    def test_access_init_wrong(self):
        """Test of initializing a bit field with a wrong 'access' value."""
        with pytest.raises(ValueError):
            BitField('bf_a', access='w0')

    def test_access_set_wrong(self):
        """Test of setting wrong value to 'access' attribute of a bit field."""
        bf = BitField('bf_a')
        with pytest.raises(ValueError):
            bf.access = 'wr'

    def test_modifiers_access(self):
        """Test of accessing to 'modifiers' attribute of a bit field."""
        bf = BitField('bf_a', access='rw')
        bf.modifiers = ['hwu']
        assert bf.modifiers == ['hwu']

    def test_modifiers_init_wrong(self):
        """Test of initializing a bit field with a wrong 'modifiers' value."""
        with pytest.raises(ValueError):
            BitField('bf_a', access='wo', modifiers=['hwu', 'rtc'])

    def test_modifiers_set_wrong(self):
        """Test of setting wrong value to 'modifiers' attribute of a bit field."""
        bf = BitField('bf_a', access='ro')
        with pytest.raises(ValueError):
            bf.modifiers = 'sc'

    def test_bits(self):
        """Test of adding a field with position that  overlaps with other field in a register."""
        bf = BitField('bf_a', lsb=5, width=4)
        assert bf.bits == [5, 6, 7, 8]

    def test_byte_strobes(self):
        """Test byte strobes info of the bit field."""
        bf_a = BitField('bf_a', lsb=0, width=16)
        bf_b = BitField('bf_b', lsb=0, width=13)
        bf_c = BitField('bf_c', lsb=8, width=16)
        bf_d = BitField('bf_d', lsb=14, width=14)
        assert bf_a.byte_strobes == {0: {'bf_lsb': 0, 'bf_msb': 7,
                                         'wdata_lsb': 0, 'wdata_msb': 7},
                                     1: {'bf_lsb': 8, 'bf_msb': 15,
                                         'wdata_lsb': 8, 'wdata_msb': 15}}
        assert bf_b.byte_strobes == {0: {'bf_lsb': 0, 'bf_msb': 7,
                                         'wdata_lsb': 0, 'wdata_msb': 7},
                                     1: {'bf_lsb': 8, 'bf_msb': 12,
                                         'wdata_lsb': 8, 'wdata_msb': 12}}
        assert bf_c.byte_strobes == {1: {'bf_lsb': 0, 'bf_msb': 7,
                                         'wdata_lsb': 8, 'wdata_msb': 15},
                                     2: {'bf_lsb': 8, 'bf_msb': 15,
                                         'wdata_lsb': 16, 'wdata_msb': 23}}
        assert bf_d.byte_strobes == {1: {'bf_lsb': 0, 'bf_msb': 1,
                                         'wdata_lsb': 14, 'wdata_msb': 15},
                                     2: {'bf_lsb': 2, 'bf_msb': 9,
                                         'wdata_lsb': 16, 'wdata_msb': 23},
                                     3: {'bf_lsb': 10, 'bf_msb': 13,
                                         'wdata_lsb': 24, 'wdata_msb': 27}}


class TestRegister:
    """Class 'Register' testing."""
    def test_create(self):
        """Test of a register creation."""
        name = 'reg_a'
        description = 'Register A'
        address = 0x4
        bfields = [
            BitField('bf_a', 'Bit field A', lsb=0),
            BitField('bf_b', 'Bit field B', lsb=1),
            BitField('bf_c', 'Bit field C', lsb=2)
        ]
        reg = Register(name, description, address)
        reg.add_bfields(bfields)
        print(repr(reg))
        print(reg)
        assert ((name, description, address, bfields) ==
                (reg.name, reg.description, reg.address, reg.bfields))

    def test_eq(self):
        """Test of equality comparision of registes."""
        reg1 = Register('reg_a')
        reg1.add_bfields([
            BitField('bf_a', 'Bit field A', lsb=0),
            BitField('bf_b', 'Bit field B', lsb=1)
        ])
        reg2 = copy.deepcopy(reg1)
        assert reg1 == reg2

    def test_ne(self):
        """Test of non equality comparision of registers."""
        reg1 = Register('reg_a')
        reg1.add_bfields([
            BitField('bf_a', 'Bit field A', lsb=0),
            BitField('bf_b', 'Bit field B', lsb=1)
        ])
        reg2 = copy.deepcopy(reg1)
        reg2['bf_a'].access = 'wo'
        assert reg1 != reg2

    def test_addr_error(self):
        """Test of a register creation with non-correct address."""
        with pytest.raises(ValueError):
            Register('reg_a', 'Register A', 'f0')

    def test_name_error_no_fields(self):
        """Test of a register creation with no name and no fields."""
        reg = Register()
        with pytest.raises(ValueError):
            reg.name

    def test_name_error_with_fields(self):
        """Test of a register creation with no name and several fields."""
        reg = Register()
        reg.add_bfields([
            BitField('bf_a', 'Bit field A', lsb=0),
            BitField('bf_b', 'Bit field B', lsb=1)
        ])
        with pytest.raises(ValueError):
            reg.name

    def test_name_of_field(self):
        """Test of a register with name and description of the field."""
        reg = Register()
        reg.add_bfields(BitField('CNT', 'Counter'))
        print(reg.name, reg.description)
        print(reg[0].name, reg.description)
        print(reg[0].name, reg[0].description)
        assert reg.name == reg[0].name
        assert reg.description == reg[0].description

    def test_add_field(self):
        """Test of adding field to a register."""
        reg = Register('REGA', 'Register A')
        bf = BitField('bf_a', 'Bit field A')
        reg.add_bfields(bf)
        assert bf == reg['bf_a']
        assert bf == reg[0]

    def test_add_fields(self):
        """Test of adding several fields to a register"""
        reg = Register('REGA', 'Register A')
        bf = [
            BitField('bf_a', 'Bit field A', lsb=0),
            BitField('bf_b', 'Bit field B', lsb=1)
        ]
        reg.add_bfields(bf)
        assert bf[0] == reg['bf_a']
        assert bf[0] == reg[0]
        assert bf[1] == reg['bf_b']
        assert bf[1] == reg[1]

    def test_get_field_key_error(self):
        """Test of trying to get bit field with wrong name."""
        reg = Register('REGA', 'Register A')
        bf = [
            BitField('bf_a', 'Bit field A', lsb=0),
            BitField('bf_b', 'Bit field B', lsb=1)
        ]
        reg.add_bfields(bf)
        with pytest.raises(KeyError):
            reg['bf_c']

    def test_get_field_index_error(self):
        """Test of trying to get bit field with wrong index."""
        reg = Register('REGA', 'Register A')
        bf = [
            BitField('bf_a', 'Bit field A', lsb=0),
            BitField('bf_b', 'Bit field B', lsb=1)
        ]
        reg.add_bfields(bf)
        with pytest.raises(KeyError):
            reg[3]

    def test_field_name_conflict(self):
        """Test of adding a field with a name that already present in a register."""
        reg = Register('REGA', 'Register A')
        reg.add_bfields(BitField('bf_a', 'Bit field A', lsb=0))
        with pytest.raises(ValueError):
            reg.add_bfields(BitField('bf_a', 'Bit field A', lsb=0))

    def test_field_position_conflict(self):
        """Test of adding a field with position that  overlaps with other field in a register."""
        reg = Register('REGA', 'Register A')
        reg.add_bfields(BitField('bf_a', 'Bit field A', lsb=0, width=8))
        reg.add_bfields(BitField('bf_b', 'Bit field B', lsb=8, width=8))
        with pytest.raises(ValueError):
            reg.add_bfields(BitField('bf_c', 'Bit field C', lsb=4, width=10))

    def test_field_order(self):
        """Test of adding fields and check that they are presented in ascending order in a register."""
        reg = Register('REGA', 'Register A')
        reg.add_bfields(BitField('bf_a', 'Bit field A', lsb=0, width=3))
        reg.add_bfields(BitField('bf_b', 'Bit field B', lsb=16, width=1))
        reg.add_bfields(BitField('bf_c', 'Bit field C', lsb=5, width=6))
        reg.add_bfields(BitField('bf_d', 'Bit field D', lsb=18, width=12))
        assert reg.names == ['bf_a', 'bf_c', 'bf_b', 'bf_d']

    def test_access_strobes_access(self):
        """Test of accessing to 'access_strobes' attribute of a register."""
        reg = Register('REGA', 'Register A')
        reg.access_strobes = True
        assert reg.access_strobes is True

    def test_access_strobes_init_wrong(self):
        """Test of initializing a register with a wrong 'access_strobes' value."""
        with pytest.raises(ValueError):
            Register('REGA', 'Register A', access_strobes='true')

    def test_access_strobes_set_wrong(self):
        """Test of setting wrong value to 'access_strobes' attribute of a register."""
        reg = Register('REGA', 'Register A')
        with pytest.raises(ValueError):
            reg.access_strobes = 0


class TestRegisterMap:
    """Class 'RegisterMap' testing."""
    def test_create(self):
        """Test of a register map creation."""
        name = 'reg_a'
        description = 'Register A'
        address = 0x4
        reg = Register(name, description, address)
        reg.add_bfields([
            BitField('bf_a', 'Bit field A', lsb=0),
            BitField('bf_b', 'Bit field B', lsb=1)
        ])
        rmap = RegisterMap()
        rmap.add_regs(reg)

        print(repr(rmap))
        print(rmap)
        assert rmap['reg_a'] == reg

    def test_eq(self):
        """Test of equality comparision of register maps."""
        reg = Register('reg_a', 'Register A', 0x4)
        reg.add_bfields([
            BitField('bf_a', 'Bit field A', lsb=0),
            BitField('bf_b', 'Bit field B', lsb=1)
        ])
        rmap1 = RegisterMap()
        rmap1.add_regs(reg)
        rmap2 = copy.deepcopy(rmap1)
        assert rmap1 == rmap2

    def test_ne(self):
        """Test of non equality comparision of register maps."""
        reg = Register('reg_a', 'Register A', 0x4)
        reg.add_bfields([
            BitField('bf_a', 'Bit field A', lsb=0),
            BitField('bf_b', 'Bit field B', lsb=1)
        ])
        rmap1 = RegisterMap()
        rmap1.add_regs(reg)
        rmap2 = copy.deepcopy(rmap1)
        rmap2['reg_a']['bf_b'].initial = 1
        assert rmap1 != rmap2

    def test_add_regs(self):
        """Test of adding several registers to a map"""
        reg_a = Register('reg_a', 'Register A', 0x8)
        reg_b = Register('reg_b', 'Register B', 0xC)
        rmap = RegisterMap()
        rmap.add_regs([reg_a, reg_b])
        assert rmap[0] == reg_a
        assert rmap['reg_a'] == reg_a
        assert rmap[1] == reg_b
        assert rmap['reg_b'] == reg_b

    def test_reg_name_conflict(self):
        """Test of adding register with a name that already present in a map."""
        rmap = RegisterMap()
        rmap.add_regs(Register('reg_a', 'Register A', 0x8))
        with pytest.raises(ValueError):
            rmap.add_regs(Register('reg_a', 'Register A copypaste', 0x8))

    def test_reg_no_addr_first(self):
        """Test of adding first register with no address to a map"""
        rmap = RegisterMap()
        with pytest.raises(ValueError):
            rmap.add_regs(Register('reg_a', 'Register A'))

    def test_reg_no_addr_no_incr(self):
        """Test of adding register with no address to a map when address auto increment is deisabled."""
        rmap = RegisterMap()
        rmap.add_regs(Register('reg_a', 'Register A', 0x0))
        with pytest.raises(ValueError):
            rmap.add_regs(Register('reg_b', 'Register B'))

    def test_reg_addr_align_data_width(self):
        """Test of adding register with address not aligned to a proper value (based on a data width)."""
        config = Configuration()
        config['regmap']['address_alignment_mode'].value = 'data_width'
        config['data_width'].value = 32
        rmap = RegisterMap(config=config)
        with pytest.raises(ValueError):
            rmap.add_regs(Register('reg_a', 'Register A', 0x2))

    def test_reg_addr_align_custom(self):
        """Test of adding register with address not aligned to a proper value (based on a custom value)."""
        config = Configuration()
        config['regmap']['address_alignment_mode'].value = 'custom'
        config['regmap']['address_alignment_value'].value = 128
        rmap = RegisterMap(config=config)
        with pytest.raises(ValueError):
            rmap.add_regs(Register('reg_a', 'Register A', 0x4))

    def test_reg_addr_align_none(self):
        """Test of adding register with address not aligned to a proper value (based on a custom value)."""
        config = Configuration()
        config['regmap']['address_alignment_mode'].value = 'none'
        config['data_width'].value = 32
        config['regmap']['address_alignment_value'].value = 128
        rmap = RegisterMap(config=config)
        # no exception
        rmap.add_regs(Register('reg_a', 'Register A', 0x2))

    def test_reg_addr_conflict(self):
        """Test of adding register with an address that already present in a map."""
        rmap = RegisterMap()
        rmap.add_regs(Register('reg_a', 'Register A', 0x0))
        with pytest.raises(ValueError):
            rmap.add_regs(Register('reg_b', 'Register B', 0x0))

    def test_reg_addr_string(self):
        """Test of adding registers with addresses represented as hexadenical string."""
        rmap = RegisterMap()
        rmap.add_regs([
            Register('reg_a', 'Register A', '0x04'),
            Register('reg_b', 'Register B', '0x08'),
            Register('reg_c', 'Register C', '0x0C'),
        ])
        assert rmap['reg_a'].address == 0x04
        assert rmap['reg_b'].address == 0x08
        assert rmap['reg_c'].address == 0x0C

    def test_reg_addr_order(self):
        """Test of adding registers and check that they are presented in ascending order in a map."""
        rmap = RegisterMap()
        rmap.add_regs(Register('reg_a', 'Register A', 0x0))
        rmap.add_regs(Register('reg_b', 'Register B', 0x10))
        rmap.add_regs(Register('reg_c', 'Register C', 0x4))
        rmap.add_regs(Register('reg_d', 'Register D', 0x14))
        assert rmap.names == ['reg_a', 'reg_c', 'reg_b', 'reg_d']

    def test_reg_addr_auto_incr_data_width(self):
        """Test of auto increment of a register's address based on interface data width."""
        config = Configuration()
        config['regmap']['address_increment_mode'].value = 'data_width'
        config['data_width'].value = 64
        rmap = RegisterMap(config=config)
        rmap.add_regs(Register('reg_a', 'Register A', 0x0))
        rmap.add_regs(Register('reg_b', 'Register B'))
        assert rmap['reg_b'].address == 0x8

    def test_reg_addr_auto_incr_custom(self):
        """Test of auto increment of a register's address."""
        config = Configuration()
        config['regmap']['address_alignment_mode'].value = 'none'
        config['regmap']['address_increment_mode'].value = 'custom'
        config['regmap']['address_increment_value'].value = 0x2
        rmap = RegisterMap(config=config)
        rmap.add_regs(Register('reg_a', 'Register A', 0x0))
        rmap.add_regs(Register('reg_b', 'Register B'))
        assert rmap['reg_b'].address == 0x2

    def test_reg_addr_auto_incr_align(self):
        """Test of alignment check of an auto incremented register's address."""
        config = Configuration()
        config['regmap']['address_alignment_mode'].value = 'custom'
        config['regmap']['address_alignment_value'].value = 0x4
        config['regmap']['address_increment_mode'].value = 'custom'
        config['regmap']['address_increment_value'].value = 0x2
        rmap = RegisterMap(config=config)
        rmap.add_regs(Register('reg_a', 'Register A', 0x0))
        with pytest.raises(ValueError):
            rmap.add_regs(Register('reg_b', 'Register B'))

    def test_bf_datawidth_conflict(self):
        """Wait exception when bf.msb value exceeds data width."""
        reg = Register('reg_a', 'Register A', 0x4)
        reg.add_bfields([
            BitField('bf_a', 'Bit field A', lsb=0, width=35),
        ])
        rmap = RegisterMap()
        with pytest.raises(ValueError):
            rmap.add_regs(reg)

    def test_compl_wr(self):
        """Wait exception when there is at least one RW field in complementary register"""
        reg = Register('reg_a', 'Register A', 0x4, complementary=True)
        reg.add_bfields([
            BitField('bf_a', 'Bit field A', lsb=0, width=16, access='rw'),
        ])
        rmap = RegisterMap()
        rmap.add_regs(reg)
        with pytest.raises(ValueError):
            rmap._validate()

    def test_compl_mixed(self):
        """Wait exception when there are 'wo' and 'ro' fields inside complementary register"""
        reg = Register('reg_a', 'Register A', 0x4, complementary=True)
        reg.add_bfields([
            BitField('bf_a', 'Bit field A', lsb=0, width=16, access='ro'),
            BitField('bf_b', 'Bit field B', lsb=16, width=16, access='wo'),
        ])
        rmap = RegisterMap()
        rmap.add_regs(reg)
        with pytest.raises(ValueError):
            rmap._validate()

    def test_compl_orphan(self):
        """Wait exception when no complementary pair found after validation"""
        reg = Register('reg_a', 'Register A', 0x4, complementary=True)
        reg.add_bfields([
            BitField('bf_a', 'Bit field A', lsb=0, width=16, access='ro'),
        ])
        rmap = RegisterMap()
        rmap.add_regs(reg)
        with pytest.raises(ValueError):
            rmap._validate()

    def test_compl_no_addr(self):
        """Address of a complementary registers must be assigned explicitly"""
        reg = Register('reg_a', 'Register A', complementary=True)
        rmap = RegisterMap()
        rmap.config['regmap']['address_increment_mode'].value = 'data_width'
        rmap.add_regs(Register('reg_a', 'Register A', 0x0))
        with pytest.raises(ValueError):
            rmap.add_regs(Register('reg_b', 'Register B', complementary=True))

    def test_compl_multiple(self):
        """Wait exception when more then 2 complementary registers are assigned to the one address."""
        rmap = RegisterMap()
        rmap.add_regs(Register('rega_w', 'Register A write part', 0x0, complementary=True))
        rmap.add_regs(Register('rega_r', 'Register A read part', 0x0, complementary=True))
        with pytest.raises(ValueError):
            rmap.add_regs(Register('rega_rr', 'Register A one more read part', 0x0, complementary=True))

    def test_compl(self):
        """Add complementary pair to register map."""
        rmap = RegisterMap()
        rmap.add_regs([
            Register('rega_w', 'Register A write part', 0x0, complementary=True),
            Register('rega_r', 'Register A read part', 0x0, complementary=True),
        ])

    def test_wlock_ro(self):
        """Exception when write_lock is active in register with no write bitfields."""
        reg = Register('rega', 'Register A', 0x0, write_lock=True)
        reg.add_bfields([
            BitField('bf_a', 'Bit field A', lsb=0, width=16, access='ro'),
        ])
        rmap = RegisterMap()
        rmap.add_regs(reg)
        with pytest.raises(ValueError):
            rmap._validate()
