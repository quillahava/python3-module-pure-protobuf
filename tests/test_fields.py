"""
`pure-protobuf` contributors © 2011-2019
"""
from io import BytesIO
from typing import List, Optional

from pytest import mark

from pure_protobuf.enums import WireType
from pure_protobuf.fields import NonRepeatedField, PackedRepeatedField, UnpackedRepeatedField
from pure_protobuf.serializers import BytesSerializer, UnsignedVarintSerializer


@mark.parametrize('value, bytes_', [
    (b'testing', b'\x0A\x07testing'),
])
def test_scalar_field(value: bytes, bytes_: bytes):
    field = NonRepeatedField(1, 'a', BytesSerializer())
    assert field.dumps(value) == bytes_
    with BytesIO(bytes_) as io:
        assert field.load(WireType(UnsignedVarintSerializer().load(io) & 0b111), io) == value


@mark.parametrize('value, expected', [
    (1, b'\x08\x01'),
    (None, b''),
])
def test_optional_scalar_field(value: Optional[int], expected: bytes):
    assert NonRepeatedField(1, 'a', UnsignedVarintSerializer()).dumps(value) == expected


@mark.parametrize('value, bytes_', [
    ([], b'\x0A\x00'),
    ([3], b'\x0A\x01\x03'),
    ([4, 5], b'\x0A\x02\x04\x05'),
])
def test_packed_repeated_field(value: List[int], bytes_: bytes):
    field = PackedRepeatedField(1, 'a', UnsignedVarintSerializer())
    assert field.dumps(value) == bytes_
    with BytesIO(bytes_) as io:
        assert field.load(WireType(UnsignedVarintSerializer().load(io) & 0b111), io) == value


@mark.parametrize('value, bytes_', [
    ([], b''),
    ([3], b'\x08\x03'),
    ([4, 5], b'\x08\x04\x08\x05'),
])
def test_unpacked_repeated_field(value: List[int], bytes_: bytes):
    assert UnpackedRepeatedField(1, 'a', UnsignedVarintSerializer()).dumps(value) == bytes_