# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.

"""Dialog configurator for the write_node_frame_limit case.

Port of the Squish write_node_limit_gui case: select a write node that
declares its own frame-range limit and submit with the override off, so the
golden's Frames parameter proves the node's limit wins over the wider scene
range (1-100).

The scene has two limited nodes, 5-10 on Write1 and 40-60 on Write2, so a
lookup that resolved the limit off the wrong node would show up as 40-60
rather than passing quietly.
"""


def configure(dialog) -> None:
    dialog.set_job_name("Write Node Frame Range Limits Job")
    dialog.set_job_description("Verify that the Write node frame range limits are respected")
    dialog.switch_to_job_specific_tab()
    dialog.select_write_node("Write1")
    assert (
        not dialog.override_frame_range_enabled()
    ), "the override must stay off for the write node's own limit to apply"
