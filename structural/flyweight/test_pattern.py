"""Tests for Flyweight Pattern."""
import pytest
from .pattern import (
    FlyweightFactory,
    TreeFactory, Tree,
    CharacterStyleFactory, Character,
    ImageFactory, ImageReference,
    ParticleFactory, ParticleInstance
)


class TestBasicFlyweight:
    def test_flyweight_factory_reuses_objects(self):
        factory = FlyweightFactory()
        fw1 = factory.get_flyweight("shared")
        fw2 = factory.get_flyweight("shared")
        assert fw1 is fw2

    def test_different_flyweights(self):
        factory = FlyweightFactory()
        fw1 = factory.get_flyweight("state1")
        fw2 = factory.get_flyweight("state2")
        assert fw1 is not fw2


class TestTreeFlyweight:
    def test_tree_shares_type(self):
        oak = TreeFactory.get_tree_type("Oak", "green", "rough")
        pine = TreeFactory.get_tree_type("Pine", "green", "smooth")
        
        assert oak is not pine
        assert TreeFactory.get_flyweight_count() == 2

    def test_multiple_trees_same_type(self):
        oak_type = TreeFactory.get_tree_type("Oak", "green", "rough")
        tree1 = Tree(0, 0, oak_type)
        tree2 = Tree(10, 10, oak_type)
        
        assert tree1.tree_type is tree2.tree_type
        assert TreeFactory.get_flyweight_count() == 1


class TestCharacterFlyweight:
    def test_character_style_sharing(self):
        style1 = CharacterStyleFactory.get_style("Arial", 12, "black")
        style2 = CharacterStyleFactory.get_style("Arial", 12, "black")
        
        assert style1 is style2

    def test_multiple_characters_same_style(self):
        style = CharacterStyleFactory.get_style("Arial", 12, "black")
        char1 = Character('A', 0, style)
        char2 = Character('B', 1, style)
        
        assert char1.style is char2.style


class TestImageFlyweight:
    def test_image_flyweight_reuse(self):
        img1 = ImageFactory.get_image("image.png")
        img2 = ImageFactory.get_image("image.png")
        
        assert img1 is img2
        assert ImageFactory.get_count() == 1

    def test_image_references(self):
        image = ImageFactory.get_image("image.png")
        ref1 = ImageReference(image, 0, 0)
        ref2 = ImageReference(image, 100, 100, 45)
        
        assert ref1.image is ref2.image
        assert ref1.x == 0
        assert ref2.x == 100


class TestParticleFlyweight:
    def test_particle_flyweight_creation(self):
        red = ParticleFactory.create_particle("red", 1.0, 1.0)
        blue = ParticleFactory.create_particle("blue", 1.0, 1.0)
        
        assert red is not blue
        assert ParticleFactory.get_count() == 2

    def test_particle_instances(self):
        particle = ParticleFactory.create_particle("red")
        p1 = ParticleInstance(particle, 0, 0)
        p2 = ParticleInstance(particle, 50, 50)
        
        p1.update(10, 10)
        p2.update(-5, -5)
        
        assert p1.x == 10
        assert p2.x == 45

