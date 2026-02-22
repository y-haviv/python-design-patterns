"""
Comprehensive tests for the Prototype pattern.

These tests verify:
1. Basic cloning functionality.
2. Deep copy independence (modifications don't affect original).
3. Prototype registry management.
4. Real-world scenarios with themed components and documents.
"""

from __future__ import annotations
import pytest
from copy import deepcopy

from .pattern import (
    Cloneable,
    DocumentSection,
    Document,
    CharacterClass,
    Skill,
    GameCharacter,
    UIComponentType,
    UIStyle,
    UIComponent,
    PrototypeRegistry,
    DocumentTemplateRegistry,
    CharacterTemplateRegistry,
    create_document_templates,
    create_character_templates,
    create_ui_component_templates,
)

from .real_world_example import (
    Color,
    Typography,
    Spacing,
    DesignTheme,
    create_light_theme_prototype,
    create_dark_theme_from_light,
    create_high_contrast_theme_from_light,
    create_compact_theme_from_light,
    ThemeLibrary,
)


class TestBasicCloning:
    """Test basic cloning functionality."""

    def test_document_clone_returns_cloneable(self):
        """Verify clone returns a Cloneable instance."""
        doc = Document(title="Test", author="Author")
        cloned = doc.clone()

        assert isinstance(cloned, Cloneable)
        assert isinstance(cloned, Document)

    def test_document_clone_creates_independent_copy(self):
        """Verify cloned document is independent from original."""
        original = Document(title="Original", author="Author")
        cloned = original.clone()

        # Modify clone
        cloned.title = "Modified"
        cloned.author = "Different Author"

        # Original should be unchanged
        assert original.title == "Original"
        assert original.author == "Author"

    def test_game_character_clone_independence(self):
        """Verify cloned character is independent."""
        warrior = GameCharacter(
            name="Warrior",
            character_class=CharacterClass.WARRIOR,
            health=100,
            strength=15
        )

        cloned = warrior.clone()
        cloned.name = "Warrior Clone"
        cloned.health = 50
        cloned.strength = 10

        # Original unchanged
        assert warrior.name == "Warrior"
        assert warrior.health == 100
        assert warrior.strength == 15

    def test_ui_component_clone_independence(self):
        """Verify cloned UI component is independent."""
        button = UIComponent(
            component_type=UIComponentType.BUTTON,
            id="btn1",
            label="Click"
        )

        cloned = button.clone()
        cloned.label = "Modified"
        cloned.width = 200

        assert button.label == "Click"
        assert button.width == 100


class TestDeepCopyBehavior:
    """Test deep copy behavior for nested objects."""

    def test_document_sections_are_deep_copied(self):
        """Verify that nested sections are deep copied."""
        original = Document(title="Doc", author="Auth")
        section = DocumentSection(title="Section 1", content="Content", page_number=1)
        original.add_section(section)

        cloned = original.clone()
        cloned.sections[0].title = "Modified Section"

        # Original section unchanged
        assert original.sections[0].title == "Section 1"
        assert cloned.sections[0].title == "Modified Section"

    def test_document_metadata_is_deep_copied(self):
        """Verify that nested metadata dictionaries are deep copied."""
        original = Document(title="Doc", author="Auth")
        original.set_metadata("nested", {"key": [1, 2, 3]})

        cloned = original.clone()
        cloned.metadata["nested"]["key"].append(4)

        # Original unchanged
        assert original.metadata["nested"]["key"] == [1, 2, 3]
        assert cloned.metadata["nested"]["key"] == [1, 2, 3, 4]

    def test_document_tags_list_is_deep_copied(self):
        """Verify that tags list is deep copied."""
        original = Document(title="Doc", author="Auth", tags=["tag1", "tag2"])
        cloned = original.clone()

        cloned.tags.append("tag3")

        # Original unchanged
        assert len(original.tags) == 2
        assert len(cloned.tags) == 3

    def test_character_skills_are_deep_copied(self):
        """Verify that character skills list is deep copied."""
        original = GameCharacter(
            name="Mage",
            character_class=CharacterClass.MAGE
        )
        original.add_skill(Skill("Fireball", 40, 2.0, 40))

        cloned = original.clone()
        cloned.add_skill(Skill("Frostbolt", 35, 1.8, 35))

        # Original has only 1 skill
        assert len(original.skills) == 1
        assert len(cloned.skills) == 2

    def test_character_inventory_is_deep_copied(self):
        """Verify that character inventory is deep copied."""
        original = GameCharacter(
            name="Rogue",
            character_class=CharacterClass.ROGUE
        )
        original.add_inventory_item("Gold", 100)

        cloned = original.clone()
        cloned.add_inventory_item("Gold", 50)

        # Original has 100 gold
        assert original.inventory["Gold"] == 100
        assert cloned.inventory["Gold"] == 150


class TestPrototypeRegistry:
    """Test prototype registry functionality."""

    def test_registry_register_and_retrieve(self):
        """Verify registry can register and retrieve prototypes."""
        registry = PrototypeRegistry()
        doc = Document(title="Template", author="Auth")

        registry.register("template", doc)
        retrieved = registry.get("template")

        assert retrieved is doc

    def test_registry_clone_creates_independent_copy(self):
        """Verify registry clone creates independent copy."""
        registry = PrototypeRegistry()
        original_doc = Document(title="Template", author="Auth")
        registry.register("template", original_doc)

        cloned_doc = registry.clone("template")
        cloned_doc.title = "Modified"

        # Original unchanged
        original_retrieved = registry.get("template")
        assert original_retrieved.title == "Template"

    def test_registry_clone_nonexistent_prototype(self):
        """Verify cloning nonexistent prototype returns None."""
        registry = PrototypeRegistry()
        result = registry.clone("nonexistent")

        assert result is None

    def test_registry_unregister(self):
        """Verify unregistering a prototype."""
        registry = PrototypeRegistry()
        doc = Document(title="Template", author="Auth")
        registry.register("template", doc)

        assert registry.get("template") is not None

        registry.unregister("template")

        assert registry.get("template") is None

    def test_registry_list_prototypes(self):
        """Verify listing registered prototypes."""
        registry = PrototypeRegistry()

        doc1 = Document(title="Doc1", author="Auth")
        doc2 = Document(title="Doc2", author="Auth")

        registry.register("doc1", doc1)
        registry.register("doc2", doc2)

        names = registry.list_prototypes()

        assert "doc1" in names
        assert "doc2" in names

    def test_registry_clear(self):
        """Verify clearing registry."""
        registry = PrototypeRegistry()
        registry.register("doc1", Document(title="D1", author="A"))
        registry.register("doc2", Document(title="D2", author="A"))

        assert len(registry.list_prototypes()) == 2

        registry.clear()

        assert len(registry.list_prototypes()) == 0


class TestDocumentTemplateRegistry:
    """Test specialized document template registry."""

    def test_create_from_template(self):
        """Verify creating document from template."""
        registry = create_document_templates()

        report1 = registry.create_from_template("annual_report")
        report1.title = "Q1 2025 Report"

        report2 = registry.create_from_template("annual_report")
        report2.title = "Q2 2025 Report"

        # Both cloned from template, independent
        assert report1.title == "Q1 2025 Report"
        assert report2.title == "Q2 2025 Report"

        # Original template unchanged
        template = registry.get("annual_report")
        assert template.title == "Annual Report"

    def test_templates_have_metadata(self):
        """Verify templates include proper metadata."""
        registry = create_document_templates()

        report = registry.create_from_template("annual_report")
        assert report.metadata.get("confidential") is True

        memo = registry.create_from_template("memo")
        assert memo.metadata.get("type") == "internal_communication"


class TestCharacterTemplateRegistry:
    """Test specialized character template registry."""

    def test_create_character_from_class(self):
        """Verify creating character from class template."""
        registry = create_character_templates()

        warrior1 = registry.create_character_from_class(CharacterClass.WARRIOR)
        warrior2 = registry.create_character_from_class(CharacterClass.WARRIOR)

        # Both have same base stats
        assert warrior1.strength == warrior2.strength
        assert warrior1.health == warrior2.health

        # But are independent
        warrior1.name = "Conan"
        warrior2.name = "Ragnar"

        assert warrior1.name != warrior2.name

    def test_character_classes_have_appropriate_stats(self):
        """Verify different classes have appropriate stat distributions."""
        registry = create_character_templates()

        warrior = registry.create_character_from_class(CharacterClass.WARRIOR)
        mage = registry.create_character_from_class(CharacterClass.MAGE)
        rogue = registry.create_character_from_class(CharacterClass.ROGUE)

        # Warriors have high health
        assert warrior.health > mage.health
        assert warrior.health > rogue.health

        # Mages have high mana
        assert mage.mana > warrior.mana
        assert mage.mana > rogue.mana

        # Rogues have high agility
        assert rogue.agility > warrior.agility
        assert rogue.agility > mage.agility

    def test_characters_have_skills(self):
        """Verify template characters have skills."""
        registry = create_character_templates()

        warrior = registry.create_character_from_class(CharacterClass.WARRIOR)
        assert len(warrior.skills) > 0

        mage = registry.create_character_from_class(CharacterClass.MAGE)
        assert len(mage.skills) > 0


class TestUIComponentCloning:
    """Test UI component prototype cloning."""

    def test_ui_component_clone_generates_new_id(self):
        """Verify cloned components get new IDs."""
        button = UIComponent(
            component_type=UIComponentType.BUTTON,
            id="btn_original",
            label="Original"
        )

        cloned = button.clone()

        # IDs should be different
        assert cloned.id != button.id
        assert "clone" in cloned.id

    def test_ui_component_style_is_cloned(self):
        """Verify component styles are properly cloned."""
        button = UIComponent(
            component_type=UIComponentType.BUTTON,
            id="btn1",
            style=UIStyle(background_color="#FF0000")
        )

        cloned = button.clone()
        cloned.style.background_color = "#00FF00"

        # Original unchanged
        assert button.style.background_color == "#FF0000"
        assert cloned.style.background_color == "#00FF00"

    def test_ui_component_handlers_are_cloned(self):
        """Verify component event handlers are cloned."""
        button = UIComponent(
            component_type=UIComponentType.BUTTON,
            id="btn1"
        )
        button.bind_handler("click", "on_click")
        button.bind_handler("hover", "on_hover")

        cloned = button.clone()
        cloned.handlers["click"] = "modified_handler"

        # Original unchanged
        assert button.handlers["click"] == "on_click"
        assert cloned.handlers["click"] == "modified_handler"


class TestThemePrototypes:
    """Test design theme prototype functionality."""

    def test_create_light_theme_prototype(self):
        """Verify light theme prototype creation."""
        theme = create_light_theme_prototype()

        assert theme.name == "Light Theme"
        assert len(theme.colors) > 0
        assert len(theme.typography.sizes) > 0

    def test_dark_theme_cloned_from_light(self):
        """Verify dark theme created by cloning light theme."""
        light = create_light_theme_prototype()
        dark = create_dark_theme_from_light(light)

        assert dark.name == "Dark Theme"
        assert dark.colors["background"].hex_code == "#1A1A1A"
        
        # Light unchanged
        assert light.colors["background"].hex_code == "#FFFFFF"

    def test_high_contrast_theme_created(self):
        """Verify high contrast theme creation."""
        light = create_light_theme_prototype()
        hc = create_high_contrast_theme_from_light(light)

        assert hc.name == "High Contrast Theme"
        # Font sizes should be increased for accessibility
        assert hc.typography.sizes["body"] > light.typography.sizes["body"]

    def test_compact_theme_created(self):
        """Verify compact theme creation."""
        light = create_light_theme_prototype()
        compact = create_compact_theme_from_light(light)

        assert compact.name == "Compact Theme"
        # Spacing should be reduced
        assert compact.spacing.values["md"] < light.spacing.values["md"]

    def test_theme_library_initialization(self):
        """Verify theme library initializes with multiple themes."""
        library = ThemeLibrary()

        themes = library.list_available_themes()
        assert "light" in themes
        assert "dark" in themes
        assert "high_contrast" in themes
        assert "compact" in themes

    def test_theme_library_get_theme_clone(self):
        """Verify theme library returns independent clones."""
        library = ThemeLibrary()

        theme1 = library.get_theme_clone("light")
        theme2 = library.get_theme_clone("light")

        # Modify first clone
        theme1.colors["primary"].hex_code = "#999999"

        # Second clone should be unchanged
        assert theme2.colors["primary"].hex_code == "#0066CC"

        # Original should also be unchanged
        original = library.get_theme("light")
        assert original.colors["primary"].hex_code == "#0066CC"

    def test_create_theme_variant(self):
        """Verify creating custom theme variants."""
        library = ThemeLibrary()

        corporate = library.create_theme_variant("light", "Corporate Theme")
        corporate.colors["primary"].hex_code = "#003366"

        # Original light theme unchanged
        light = library.get_theme("light")
        assert light.colors["primary"].hex_code == "#0066CC"


class TestPerformanceBenefit:
    """Test performance benefits of prototype pattern."""

    def test_cloning_is_cheaper_than_initialization(self):
        """Demonstrate that cloning is viable for rapid object creation."""
        # Create prototype once
        prototype = create_light_theme_prototype()

        # Clone many times (should be fast)
        variants = []
        for i in range(100):
            variant = prototype.clone()
            variant.name = f"Variant {i}"
            variants.append(variant)

        # All should exist and be independent
        assert len(variants) == 100
        assert all(isinstance(v, DesignTheme) for v in variants)
        assert len(set(v.name for v in variants)) == 100  # All unique names


class TestIntegrationScenarios:
    """Integration tests with realistic scenarios."""

    def test_document_workflow(self):
        """Test realistic document workflow using prototypes."""
        registry = create_document_templates()

        # Create multiple reports from template
        q1_report = registry.create_from_template("annual_report")
        q1_report.title = "Q1 2025 Report"

        q2_report = registry.create_from_template("annual_report")
        q2_report.title = "Q2 2025 Report"

        # Both are independent and properly templated
        assert q1_report.metadata["confidential"] == q2_report.metadata["confidential"]
        assert q1_report.title != q2_report.title

    def test_game_character_generation(self):
        """Test realistic game character generation."""
        registry = create_character_templates()

        # Create party of mixed classes
        party = [
            registry.create_character_from_class(CharacterClass.WARRIOR),
            registry.create_character_from_class(CharacterClass.MAGE),
            registry.create_character_from_class(CharacterClass.ROGUE),
        ]

        # All should have appropriate characteristics
        assert party[0].character_class == CharacterClass.WARRIOR
        assert party[1].character_class == CharacterClass.MAGE
        assert party[2].character_class == CharacterClass.ROGUE

        # All should be independent
        party[0].level_up()
        assert party[1].level == 1

    def test_ui_component_template_system(self):
        """Test UI component templating system."""
        registry = create_ui_component_templates()

        # Create multiple buttons from template
        button1 = registry.clone("primary_button")
        button1.set_position(10, 10)

        button2 = registry.clone("primary_button")
        button2.set_position(150, 10)

        # Both buttons should have consistent styling
        assert button1.style.background_color == button2.style.background_color

        # But different positions
        assert button1.x_position != button2.x_position
