import logging
from openedx.core.lib.block_cache.transformer import BlockStructureTransformer


class StudentViewTransformer(BlockStructureTransformer):
    """
    ...
    """
    VERSION = 1
    STUDENT_VIEW_DATA = 'student_view_data'
    STUDENT_VIEW_MULTI_DEVICE = 'student_view_multi_device'

    def __init__(self, requested_student_view_data):
        self.requested_student_view_data = requested_student_view_data

    @classmethod
    def collect(cls, block_structure):
        """
        Collect student_view_multi_device and student_view_data values for each block
        """
        # TODO
        # File "/edx/app/edxapp/edx-platform/common/lib/xmodule/xmodule/x_module.py", line 1125, in _xmodule
        #     raise UndefinedContext()
        # import pdb; pdb.set_trace()

        for block_key in block_structure.topological_traversal():
            block = block_structure.get_xblock(block_key)
            try:
                #if block_key.block_type == "problem":
                #    import pudb; pu.db
                student_view = getattr(block.__class__, 'student_view', None)
                supports_multi_device = block.has_support(student_view, 'multi_device')
            except Exception as e:
                print "SKIPPING: {} cause {}".format(block.location, e)
                supports_multi_device = False
            else:
                print "supports_multi_device: {!s:5} => {}".format(supports_multi_device, block.location)

            block_structure.set_transformer_block_data(
                block_key,
                cls,
                cls.STUDENT_VIEW_MULTI_DEVICE,
                supports_multi_device,
            )
            if getattr(block, 'student_view_data', None):
#                import pudb; pu.db
                try:
                    student_view_data = block.student_view_data()
                except Exception as e:
                    student_view_data = {}
                    print "Error executing student_view_data: {}".format(e)

                block_structure.set_transformer_block_data(
                    block_key,
                    cls,
                    cls.STUDENT_VIEW_DATA,
                    student_view_data,
                )

    def transform(self, user_info, block_structure):
        """
        Mutates block_structure based on the given user_info.
        """
        for block_key in block_structure.post_order_traversal():
            if block_structure.get_xblock_field(block_key, 'type') not in self.requested_student_view_data:
                block_structure.remove_transformer_block_data(block_key, self, self.STUDENT_VIEW_DATA)
