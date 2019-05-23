from f5.bigip import ManagementRoot


class F5Manager:
    mgmt = None

    def connect(self):
        # Connect to the BigIP
        self.mgmt = ManagementRoot("localhost", "vagrant", "vagrant", port=10443)

    def is_connected(self):
        return self.mgmt is not None

    # Virtuals collection
    def get_virtuals(self):
        assert self.mgmt is not None
        return self.mgmt.tm.ltm.virtuals.get_collection()

    # Virtual
    def get_virtual(self, **kwargs):
        assert self.mgmt is not None
        return self.mgmt.tm.ltm.virtuals.virtual.load(**kwargs)

    def create_virtual(self, **kwargs):
        assert self.mgmt is not None
        self.mgmt.tm.ltm.virtuals.virtual.create(**kwargs)

    def update_virtual(self, **kwargs):
        assert self.mgmt is not None
        v = self.mgmt.tm.ltm.virtuals.virtual.load(
            name=kwargs["name"], partition=kwargs["partition"]
        )
        if "source" in kwargs:
            v.source = kwargs["source"]
        if "destination" in kwargs:
            v.destination = kwargs["destination"]
        if "description" in kwargs:
            v.description = kwargs["description"]
        v.update()

    def delete_virtual(self, **kwargs):
        assert self.mgmt is not None
        if self.mgmt.tm.ltm.virtuals.virtual.exists(**kwargs):
            virtual = self.mgmt.tm.ltm.virtuals.virtual.load(**kwargs)
            virtual.delete()
