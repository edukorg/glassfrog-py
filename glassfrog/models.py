from datetime import datetime

from glassfrog import exceptions
from glassfrog.client import GlassFrogClient


class BaseModel:
    _RESOURCE_NAME = None

    def __init__(self, data, linked_data=None):
        if not isinstance(data, dict):
            raise exceptions.UnexpectedDataFormat()

        self._data = data
        self._linked_data = linked_data

    @property
    def id(self):
        return self._get('id')

    def _get(self, value):
        try:
            return self._data[value]
        except (KeyError, TypeError):
            raise exceptions.UnexpectedDataFormat()

    def _build_item_from_link(self, link_name, model_klass):
        links = self._get('links')
        item_id = links[link_name]
        if item_id:
            try:
                return model_klass.get(id=item_id)
            except exceptions.UnsupportedModelException:
                return model_klass.build(id=item_id, linked_data=self._linked_data)
        else:
            return None

    def _build_items_from_link(self, link_name, model_klass):
        links = self._get('links')
        for item_id in links[link_name]:
            try:
                yield model_klass.get(id=item_id)
            except exceptions.UnsupportedModelException:
                yield model_klass.build(id=item_id, linked_data=self._linked_data)

    @classmethod
    def build(cls, id, linked_data):
        if linked_data:
            for data in linked_data[cls._RESOURCE_NAME]:
                if data['id'] == id:
                    return cls(data=data, linked_data=None)
        return cls(data={'id': id})

    @classmethod
    def get(cls, id):
        data = GlassFrogClient.get(resource=cls._RESOURCE_NAME, id=id)
        linked_data = data.get('linked', None)
        return cls(data=data[cls._RESOURCE_NAME][0], linked_data=linked_data)

    @classmethod
    def list(cls):
        data = GlassFrogClient.get(resource=cls._RESOURCE_NAME)
        linked_data = data.get('linked', None)
        for item in data[cls._RESOURCE_NAME]:
            yield cls(data=item, linked_data=linked_data)

    def _detail(self, resource_class):
        data = GlassFrogClient.get(
            resource=resource_class._RESOURCE_NAME,
            id=self.id,
            from_resource=self._RESOURCE_NAME,
        )
        linked_data = data.get('linked', None)
        for item in data[resource_class._RESOURCE_NAME]:
            yield resource_class(data=item, linked_data=linked_data)


class UnsupportedModelMixin:
    @classmethod
    def get(cls, id):
        raise exceptions.UnsupportedModelException()

    @classmethod
    def list(cls):
        raise exceptions.UnsupportedModelException()

    def _detail(self, resource_class):
        raise exceptions.UnsupportedModelException()


class Circle(BaseModel):
    _RESOURCE_NAME = 'circles'

    @property
    def name(self):
        return self._get('name')

    @property
    def short_name(self):
        return self._get('short_name')

    @property
    def strategy(self):
        return self._get('strategy')

    @property
    def organization(self):
        organization_id = self._get('organization_id')
        return Organization.build(id=organization_id, linked_data=self._linked_data)

    @property
    def roles(self):
        yield from self._build_items_from_link(
            link_name='roles',
            model_klass=Role,
        )

    @property
    def policies(self):
        yield from self._build_items_from_link(
            link_name='policies',
            model_klass=Policy,
        )

    @property
    def domains(self):
        yield from self._build_items_from_link(
            link_name='domain',
            model_klass=Domain,
        )

    @property
    def supported_role(self):
        return self._build_item_from_link(
            link_name='supported_role',
            model_klass=Role,
        )

    @property
    def projects(self):
        yield from self._detail(resource_class=Project)


class Person(BaseModel):
    _RESOURCE_NAME = 'people'

    @property
    def name(self):
        return self._get('name')

    @property
    def email(self):
        return self._get('email')

    @property
    def organizations(self):
        yield from self._build_items_from_link(
            link_name='organization_ids',
            model_klass=Organization,
        )

    @property
    def circles(self):
        yield from self._build_items_from_link(
            link_name='circles',
            model_klass=Circle,
        )

    @property
    def assignments(self):
        yield from self._detail(resource_class=Assignment)


class Role(BaseModel):
    _RESOURCE_NAME = 'roles'

    @property
    def name(self):
        return self._get('name')

    @property
    def short_name(self):
        return self._get('short_name')

    @property
    def organization(self):
        organization_id = self._get('organization_id')
        return Organization.build(id=organization_id, linked_data=self._linked_data)

    @property
    def is_core(self):
        return self._get('is_core')

    @property
    def purpose(self):
        return self._get('purpose')

    @property
    def circle(self):
        return self._build_item_from_link(
            link_name='circle',
            model_klass=Circle,
        )

    @property
    def supporting_circle(self):
        return self._build_item_from_link(
            link_name='supporting_circle',
            model_klass=Circle,
        )

    @property
    def domains(self):
        yield from self._build_items_from_link(
            link_name='domains',
            model_klass=Domain,
        )

    @property
    def accountabilities(self):
        yield from self._build_items_from_link(
            link_name='accountabilities',
            model_klass=Accountability,
        )

    @property
    def people(self):
        yield from self._build_items_from_link(
            link_name='people',
            model_klass=Person,
        )

    @property
    def elected_until(self):
        try:
            date_str = self._get('elected_until')
            return datetime.strptime(date_str, '%Y-%m-%d').date()
        except exceptions.UnexpectedDataFormat:
            return None

    @property
    def assignments(self):
        yield from self._detail(resource_class=Assignment)


class Assignment(BaseModel):
    _RESOURCE_NAME = 'assignments'

    @property
    def focus(self):
        return self._get('focus')

    @property
    def election(self):
        try:
            date_str = self._get('election')
            return datetime.strptime(date_str, '%Y-%m-%d').date()
        except (exceptions.UnexpectedDataFormat, TypeError):
            return None

    @property
    def exclude_from_meetings(self):
        return self._get('exclude_from_meetings')

    @property
    def person(self):
        return self._build_item_from_link(
            link_name='person',
            model_klass=Person,
        )

    @property
    def role(self):
        return self._build_item_from_link(
            link_name='role',
            model_klass=Role,
        )


class Organization(UnsupportedModelMixin, BaseModel):
    _RESOURCE_NAME = 'organizations'


class Domain(UnsupportedModelMixin, BaseModel):
    _RESOURCE_NAME = 'domains'

    @property
    def description(self):
        return self._get('description')


class Policy(UnsupportedModelMixin, BaseModel):
    _RESOURCE_NAME = 'policies'

    @property
    def title(self):
        return self._get('title')

    @property
    def body(self):
        return self._get('body')


class Accountability(UnsupportedModelMixin, BaseModel):
    _RESOURCE_NAME = 'accountabilities'

    @property
    def description(self):
        return self._get('description')


class Project(UnsupportedModelMixin, BaseModel):
    _RESOURCE_NAME = 'projects'
