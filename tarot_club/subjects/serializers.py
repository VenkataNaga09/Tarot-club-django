from rest_framework import serializers

from subjects import models

TAROT_CARDS = [
    "The Fool", "The Magician", "The High Priestess", "The Empress",
    "The Emperor", "The Hierophant", "The Lovers", "The Chariot",
    "Strength", "The Hermit", "Wheel of Fortune", "Justice",
    "The Hanged Man", "Death", "Temperance", "The Devil",
    "The Tower", "The Star", "The Moon", "The Sun",
    "Judgment", "The World"
]


class HelloSerializer(serializers.Serializer):
    """Serializes a name field for testing our APIView"""
    name = serializers.CharField(max_length=20)


class SubjectProfileSerializer(serializers.ModelSerializer):
    """Serializes a subject profile object"""
    tarot_card_name = serializers.ChoiceField(choices=TAROT_CARDS)

    class Meta:
        model = models.SubjectProfile
        fields = ('id', 'email', 'name', 'tarot_card_name', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }

    def validate_tarot_card_name(self, value):
        """Ensure the selected tarot card is not already taken."""
        if models.SubjectProfile.objects.filter(tarot_card_name=value).exists():
            raise serializers.ValidationError("This tarot card has already been chosen. Please select another.")
        return value

    def create(self, validated_data):
        """Create and return a new subject"""
        subject = models.SubjectProfile.objects.create(
            email=validated_data['email'],
            name=validated_data['name'],
            tarot_card_name=validated_data['tarot_card_name']
        )
        subject.set_password(validated_data['password'])  # Encrypt the password
        subject.save()
        return subject
    

class ProfileFeedItemSerializer(serializers.ModelSerializer):
    """Serializes profile feed items"""

    class Meta:
        model = models.ProfileFeedItem
        fields = ('id', 'subject_profile', 'content', 'created_on')
        extra_kwargs = {'subject_profile': {'read_only': True}}
