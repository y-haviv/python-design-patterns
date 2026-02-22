"""
Comprehensive tests for the Bridge Pattern.

These tests verify:
1. Basic bridge with abstraction and implementor.
2. Multiple concrete implementors.
3. Refined abstractions.
4. Runtime implementation switching.
5. Real-world remote control scenario with multiple device types and protocols.
"""

from __future__ import annotations
import pytest
from .pattern import (
    Implementor,
    ConcreteImplementorA,
    ConcreteImplementorB,
    Abstraction,
    RefinedAbstraction,
    DrawingAPI,
    CanvasAPI,
    SVGAPI,
    Shape,
    Circle,
    Rectangle,
    Line,
    ShapeComposer,
)
from .real_world_example import (
    CommunicationBridge,
    WiFiBridge,
    BluetoothBridge,
    InfraredBridge,
    RemoteControl,
    TVRemote,
    StereoRemote,
    ProjectorRemote,
    RemoteControlFactory,
)


class TestBasicBridge:
    """Tests for basic bridge functionality."""

    def test_abstraction_with_implementor_a(self) -> None:
        """Verify abstraction works with implementor A."""
        impl_a = ConcreteImplementorA()
        abstraction = Abstraction(impl_a)

        result = abstraction.operation()

        assert "Abstraction" in result
        assert "platform A" in result

    def test_abstraction_with_implementor_b(self) -> None:
        """Verify abstraction works with implementor B."""
        impl_b = ConcreteImplementorB()
        abstraction = Abstraction(impl_b)

        result = abstraction.operation()

        assert "Abstraction" in result
        assert "platform B" in result

    def test_switch_implementor_at_runtime(self) -> None:
        """Verify implementor can be switched at runtime."""
        impl_a = ConcreteImplementorA()
        abstraction = Abstraction(impl_a)

        result_a = abstraction.operation()
        assert "platform A" in result_a

        impl_b = ConcreteImplementorB()
        abstraction.set_implementor(impl_b)

        result_b = abstraction.operation()
        assert "platform B" in result_b


class TestRefinedAbstraction:
    """Tests for refined abstraction."""

    def test_refined_abstraction_extends_functionality(self) -> None:
        """Verify refined abstraction extends basic functionality."""
        impl = ConcreteImplementorA()
        refined = RefinedAbstraction(impl)

        result = refined.operation()

        assert "RefinedAbstraction" in result
        assert "Extended functionality" in result

    def test_refined_abstraction_extended_operation(self) -> None:
        """Verify refined abstraction has additional operations."""
        impl = ConcreteImplementorA()
        refined = RefinedAbstraction(impl)

        result = refined.extended_operation()

        assert "RefinedAbstraction" in result
        assert "Extended implementation detail" in result

    def test_refined_abstraction_with_different_implementors(self) -> None:
        """Verify refined abstraction works with any implementor."""
        impl_a = ConcreteImplementorA()
        impl_b = ConcreteImplementorB()

        refined_a = RefinedAbstraction(impl_a)
        refined_b = RefinedAbstraction(impl_b)

        result_a = refined_a.operation()
        result_b = refined_b.operation()

        assert "platform A" in result_a
        assert "platform B" in result_b


class TestDrawingShapes:
    """Tests for shape drawing with different APIs."""

    def test_circle_with_canvas_api(self) -> None:
        """Verify circle drawing with Canvas API."""
        api = CanvasAPI()
        circle = Circle(10, 20, 5, api)

        result = circle.draw()

        assert "Canvas" in result
        assert "circle" in result.lower()

    def test_circle_with_svg_api(self) -> None:
        """Verify circle drawing with SVG API."""
        api = SVGAPI()
        circle = Circle(10, 20, 5, api)

        result = circle.draw()

        assert "SVG" in result
        assert "circle" in result.lower()

    def test_rectangle_with_canvas_api(self) -> None:
        """Verify rectangle drawing with Canvas API."""
        api = CanvasAPI()
        rect = Rectangle(0, 0, 100, 50, api)

        result = rect.draw()

        assert "Canvas" in result
        assert "rectangle" in result.lower()

    def test_rectangle_with_svg_api(self) -> None:
        """Verify rectangle drawing with SVG API."""
        api = SVGAPI()
        rect = Rectangle(0, 0, 100, 50, api)

        result = rect.draw()

        assert "SVG" in result
        assert "rect" in result.lower()

    def test_line_with_canvas_api(self) -> None:
        """Verify line drawing with Canvas API."""
        api = CanvasAPI()
        line = Line(0, 0, 100, 100, api)

        result = line.draw()

        assert "Canvas" in result
        assert "line" in result.lower()

    def test_switch_drawing_api(self) -> None:
        """Verify drawing API can be switched."""
        canvas = CanvasAPI()
        svg = SVGAPI()

        circle = Circle(10, 10, 5, canvas)
        assert "Canvas" in circle.draw()

        circle.set_drawing_api(svg)
        assert "SVG" in circle.draw()

    def test_shape_modifications(self) -> None:
        """Verify shapes can be modified."""
        api = CanvasAPI()

        circle = Circle(5, 5, 10, api)
        circle.resize(20)
        assert circle.radius == 20

        rect = Rectangle(0, 0, 100, 50, api)
        rect.scale(2)
        assert rect.width == 200
        assert rect.height == 100

        line = Line(0, 0, 10, 10, api)
        line.extend(5, 5)
        assert line.x2 == 15
        assert line.y2 == 15


class TestShapeComposer:
    """Tests for composing multiple shapes."""

    def test_add_shapes_to_composer(self) -> None:
        """Verify adding shapes to composer."""
        api = CanvasAPI()
        composer = ShapeComposer(api)

        circle = Circle(5, 5, 10, api)
        rect = Rectangle(0, 0, 100, 50, api)

        composer.add_shape(circle)
        composer.add_shape(rect)

        assert len(composer.shapes) == 2

    def test_draw_all_shapes(self) -> None:
        """Verify drawing all shapes."""
        api = CanvasAPI()
        composer = ShapeComposer(api)

        composer.add_shape(Circle(5, 5, 10, api))
        composer.add_shape(Rectangle(0, 0, 100, 50, api))

        results = composer.draw_all()

        assert len(results) == 2
        assert all("Canvas" in result for result in results)

    def test_switch_api_for_all_shapes(self) -> None:
        """Verify switching API for all shapes."""
        canvas = CanvasAPI()
        svg = SVGAPI()

        composer = ShapeComposer(canvas)
        composer.add_shape(Circle(5, 5, 10, canvas))
        composer.add_shape(Rectangle(0, 0, 100, 50, canvas))

        results_1 = composer.draw_all()
        assert all("Canvas" in result for result in results_1)

        composer.switch_api(svg)
        results_2 = composer.draw_all()
        assert all("SVG" in result for result in results_2)


class TestWiFiBridge:
    """Tests for WiFi communication bridge."""

    def test_wifi_connect(self) -> None:
        """Verify WiFi connection."""
        bridge = WiFiBridge()

        result = bridge.connect("tv_living_room")

        assert result
        assert "tv_living_room" in bridge.connected_devices

    def test_wifi_send_command(self) -> None:
        """Verify sending command via WiFi."""
        bridge = WiFiBridge()
        bridge.connect("tv_living_room")

        result = bridge.send_command("tv_living_room", "power_on")

        assert result
        assert len(bridge.log) > 1

    def test_wifi_receive_status(self) -> None:
        """Verify receiving status via WiFi."""
        bridge = WiFiBridge()

        status = bridge.receive_status("tv_living_room")

        assert status["status"] == "online"
        assert status["protocol"] == "WiFi"

    def test_wifi_disconnect(self) -> None:
        """Verify WiFi disconnection."""
        bridge = WiFiBridge()
        bridge.connect("tv_living_room")

        result = bridge.disconnect("tv_living_room")

        assert result
        assert "tv_living_room" not in bridge.connected_devices

    def test_wifi_get_connection_type(self) -> None:
        """Verify WiFi bridge type."""
        bridge = WiFiBridge()

        assert bridge.get_connection_type() == "WiFi"


class TestBluetoothBridge:
    """Tests for Bluetooth communication bridge."""

    def test_bluetooth_connect(self) -> None:
        """Verify Bluetooth pairing."""
        bridge = BluetoothBridge()

        result = bridge.connect("stereo_bedroom")

        assert result
        assert "stereo_bedroom" in bridge.paired_devices

    def test_bluetooth_send_command(self) -> None:
        """Verify sending command via Bluetooth."""
        bridge = BluetoothBridge()
        bridge.connect("stereo_bedroom")

        result = bridge.send_command("stereo_bedroom", "play")

        assert result

    def test_bluetooth_receive_status(self) -> None:
        """Verify receiving status via Bluetooth."""
        bridge = BluetoothBridge()

        status = bridge.receive_status("stereo_bedroom")

        assert status["status"] == "paired"
        assert status["protocol"] == "Bluetooth"

    def test_bluetooth_get_connection_type(self) -> None:
        """Verify Bluetooth bridge type."""
        bridge = BluetoothBridge()

        assert bridge.get_connection_type() == "Bluetooth"


class TestInfraredBridge:
    """Tests for Infrared communication bridge."""

    def test_infrared_connect(self) -> None:
        """Verify infrared range."""
        bridge = InfraredBridge()

        result = bridge.connect("projector_office")

        assert result
        assert "projector_office" in bridge.in_range_devices

    def test_infrared_send_command(self) -> None:
        """Verify sending command via Infrared."""
        bridge = InfraredBridge()
        bridge.connect("projector_office")

        result = bridge.send_command("projector_office", "focus")

        assert result

    def test_infrared_get_connection_type(self) -> None:
        """Verify Infrared bridge type."""
        bridge = InfraredBridge()

        assert bridge.get_connection_type() == "Infrared"


class TestTVRemote:
    """Tests for TV remote control."""

    def test_tv_remote_power_operations(self) -> None:
        """Verify TV power operations."""
        bridge = WiFiBridge()
        remote = TVRemote("tv_1", bridge)

        remote.connect()
        assert remote.power_on()
        assert remote.power_off()

    def test_tv_remote_channel_control(self) -> None:
        """Verify TV channel control."""
        bridge = WiFiBridge()
        remote = TVRemote("tv_1", bridge)

        remote.connect()
        assert remote.change_channel(5)

    def test_tv_remote_volume_control(self) -> None:
        """Verify TV volume control."""
        bridge = WiFiBridge()
        remote = TVRemote("tv_1", bridge)

        remote.connect()
        assert remote.set_volume(50)
        assert remote.increase_volume()
        assert remote.decrease_volume()

    def test_tv_remote_with_different_bridges(self) -> None:
        """Verify TV remote works with different bridges."""
        wifi = WiFiBridge()
        ir = InfraredBridge()

        remote = TVRemote("tv_1", wifi)
        remote.connect()
        assert remote.power_on()

        remote.change_communication(ir)
        remote.connect()
        assert remote.power_on()


class TestStereoRemote:
    """Tests for stereo remote control."""

    def test_stereo_remote_play_operations(self) -> None:
        """Verify stereo play operations."""
        bridge = BluetoothBridge()
        remote = StereoRemote("stereo_1", bridge)

        remote.connect()
        assert remote.play()
        assert remote.pause()
        assert remote.stop()

    def test_stereo_remote_track_control(self) -> None:
        """Verify stereo track control."""
        bridge = BluetoothBridge()
        remote = StereoRemote("stereo_1", bridge)

        remote.connect()
        assert remote.next_track()
        assert remote.previous_track()

    def test_stereo_remote_volume(self) -> None:
        """Verify stereo volume control."""
        bridge = BluetoothBridge()
        remote = StereoRemote("stereo_1", bridge)

        remote.connect()
        assert remote.set_volume(75)


class TestProjectorRemote:
    """Tests for projector remote control."""

    def test_projector_remote_power(self) -> None:
        """Verify projector power control."""
        bridge = InfraredBridge()
        remote = ProjectorRemote("projector_1", bridge)

        remote.connect()
        assert remote.power_on()
        assert remote.power_off()

    def test_projector_remote_focus_zoom(self) -> None:
        """Verify projector focus and zoom."""
        bridge = InfraredBridge()
        remote = ProjectorRemote("projector_1", bridge)

        remote.connect()
        assert remote.focus("in")
        assert remote.zoom(1.5)

    def test_projector_remote_brightness(self) -> None:
        """Verify projector brightness control."""
        bridge = InfraredBridge()
        remote = ProjectorRemote("projector_1", bridge)

        remote.connect()
        assert remote.brightness(80)


class TestRemoteControlFactory:
    """Tests for remote control factory."""

    def test_factory_create_tv_remote(self) -> None:
        """Verify factory creates TV remote."""
        factory = RemoteControlFactory()
        bridge = WiFiBridge()

        remote = factory.create_tv_remote("tv_1", bridge)

        assert isinstance(remote, TVRemote)
        assert "tv_1" in factory.remotes

    def test_factory_create_stereo_remote(self) -> None:
        """Verify factory creates stereo remote."""
        factory = RemoteControlFactory()
        bridge = BluetoothBridge()

        remote = factory.create_stereo_remote("stereo_1", bridge)

        assert isinstance(remote, StereoRemote)
        assert "stereo_1" in factory.remotes

    def test_factory_create_multiple_remotes(self) -> None:
        """Verify factory can create multiple remotes."""
        factory = RemoteControlFactory()
        wifi = WiFiBridge()
        bt = BluetoothBridge()
        ir = InfraredBridge()

        factory.create_tv_remote("tv_1", wifi)
        factory.create_stereo_remote("stereo_1", bt)
        factory.create_projector_remote("projector_1", ir)

        remotes = factory.get_all_remotes()
        assert len(remotes) == 3
        assert isinstance(remotes["tv_1"], TVRemote)
        assert isinstance(remotes["stereo_1"], StereoRemote)
        assert isinstance(remotes["projector_1"], ProjectorRemote)

