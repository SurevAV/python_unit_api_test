import pytest
from prj import FakeWebService
import copy


class Test_get_items:
    def test_get_items(self):
        """
        Should return_all items from service (200)
        """

        # Act
        answer, data = FakeWebService.get_items()
        # Assert
        assert answer == 200
        assert str(data) == str(FakeWebService.Data) 


class Test_get_item:
    def test_get_item_with_exist_id(self):
        """
        Should return exist item by id (200)
        """

        # Arrange
        id_item = 1

        # Act
        answer, data = FakeWebService.get_item(id_item)

        # Assert
        assert answer == 200
        assert str(data) == str(FakeWebService.Data[id_item])

    def test_get_item_with_non_existent_id(self):
        """
        Should return Not found (404)
        """

        # Arrange
        id_item = 'non_existent_id'

        # Act
        answer, data = FakeWebService.get_item(id_item)

        # Assert
        assert answer == 404
        assert str(data) == 'Not found'

    def test_get_item_with_non_value(self):
        """
        Should return Not found (404)
        """

        # Arrange
        id_item = ''

        # Act
        answer, data = FakeWebService.get_item(id_item)

        # Assert
        assert answer == 404
        assert str(data) == 'Not found'


class Test_patch_decrease:
    def test_patch_decrease_with_exist_id(self):
        """
        Should return changed record (200)
        """

        # Arrange
        id_item = 1
        answer, check_data = FakeWebService.get_item(id_item)
        check_data = copy.copy(check_data)
        amount = check_data['amount']
        qty = check_data['qty']
        price = amount / qty
        check_data['qty'] = qty - 1
        check_data['amount'] = price * check_data['qty']
    
        # Act
        answer, data = FakeWebService.patch_decrease(id_item)

        # Assert
        assert answer == 200
        assert data['qty'] == check_data['qty']
        assert data['amount'] == check_data['amount']

    # patch_decrease not checking id parametr on exist(test fail 1)
    def test_patch_decrease_with_not_exist_id(self):
        """
        Should return Not found (404)
        """
    
        # Act
        answer, data = FakeWebService.patch_decrease(20)

        # Assert
        assert answer == 404
        assert data is None


class Test_patch_increase:
    def test_patch_increase_with_exist_id(self):
        """
        Should return changed record (200)
        """

        # Arrange
        id_item = 1
        answer, check_data = FakeWebService.get_item(id_item)
        check_data = copy.copy(check_data)
        amount = check_data['amount']
        qty = check_data['qty']
        price = amount / qty
        check_data['qty'] = qty + 1
        check_data['amount'] = price * check_data['qty']
    
        # Act
        answer, data = FakeWebService.patch_increase(id_item)

        # Assert
        assert answer == 200
        assert data['qty'] == check_data['qty']
        assert data['amount'] == check_data['amount']

    # patch_decrease not checking id parametr on exist(test fail 2)
    def test_patch_increase_with_not_exist_id(self):
        """
        Should return Not found (404)
        """
    
        # Act
        answer, data = FakeWebService.patch_increase(20)

        # Assert
        assert answer == 404
        assert data is None


class Test_post_item:
    # post_item not checking item(test fail 3)
    def test_post_item_with_wrong_item(self):
        """
        Should return BadRequest (400)
        """

        # Arrange
        item = {'wrong':4}

        # Act
        answer, data = FakeWebService.post_item(item)

        # Assert
        assert answer == 400
        assert str(data) == 'BadRequest'

    def test_post_item_with_none_id(self):
        """
        Should return BadRequest (400)
        """

        # Arrange
        item = {'id': None, 'name': 'new name', 'amount': 5, 'qty': 4}

        # Act
        answer, data = FakeWebService.post_item(item)

        # Assert
        assert answer == 400
        assert str(data) == 'BadRequest'

    def test_post_item_with_none_name(self):
        """
        Should return BadRequest (400)
        """

        # Arrange
        item = {'id': 1, 'name': None, 'amount': 5, 'qty': 4}

        # Act
        answer, data = FakeWebService.post_item(item)

        # Assert
        assert answer == 400
        assert str(data) == 'BadRequest'

    def test_post_item_with_none_amount(self):
        """
        Should return BadRequest (400)
        """

        # Arrange
        item = {'id': 1, 'name': 'new name', 'amount': None, 'qty': 4}

        # Act
        answer, data = FakeWebService.post_item(item)

        # Assert
        assert answer == 400
        assert str(data) == 'BadRequest'

    # post_item not checking qty parametr on None value(test fail 4)
    def test_post_item_with_none_qty(self):
        """
        Should return BadRequest (400)
        """

        # Arrange
        item = {'id': 10, 'name': 'new name', 'amount': 2, 'qty': None}

        # Act
        answer, data = FakeWebService.post_item(item)

        # Assert
        assert answer == 400
        assert str(data) == 'BadRequest'

    def test_post_item_with_exist_name(self):
        """
        Should return Already existed (400)
        """

        # Arrange
        item = {'id': 1, 'name': 'test2', 'amount': 2, 'qty': 5}

        # Act
        answer, data = FakeWebService.post_item(item)

        # Assert
        assert answer == 400
        assert str(data) == 'Already existed'

    def test_post_item_with_item_with_not_exist_id(self):
        """
        Should make new record in service and return None (200)
        """

        # Arrange
        id_item = 0
        item = {'id': id_item, 'name': 'test name', 'amount': 2, 'qty': 5}

        # Act
        answer, data = FakeWebService.post_item(item)

        # Assert
        assert answer == 200
        assert data is None
        answer, data = FakeWebService.get_item(id_item)
        assert answer == 200
        assert str(data) == str(item)

    def test_post_item_with_item_with_exist_id(self):
        """
        Should change exist record in service and return None (200)
        """

        # Arrange
        id_item = 3
        item = {'id': id_item, 'name': 'test name 2', 'amount': 2, 'qty': 5}

        # Act
        answer, data = FakeWebService.post_item(item)

        # Assert
        assert answer == 200
        assert data is None
        answer, data = FakeWebService.get_item(id_item)
        assert answer == 200
        assert str(data) == str(item)


class Test_post_bucket:
    
    # post_bucket not return answer(test fail 5)
    def test_post_bucket_with_many_items(self):
        """
        Should return None (200)
        """

        # Arrange
        items = {1: {'name': 'name2 test1', 'amount': 100, 'qty': 4},
                 50: {'name': 'name2 test2', 'amount': 525, 'qty': 5}}
        # Act
        answer, data = FakeWebService.post_bucket(items)

        # Assert
        assert answer == 200
        assert data == None
        answer, data = FakeWebService.get_item(1)
        assert answer == 200
        assert str(data) == str(items[1])
        answer, data = FakeWebService.get_item(50)
        assert answer == 200
        assert str(data) == str(items[2])

    # post_bucket not checking value(test fail 6)
    def test_post_bucket_with_many_wrong_items(self):
        """
        Should return BadRequest (400)
        """

        # Arrange
        items = {1: {},
                 50: {}}
        # Act
        answer, data = FakeWebService.post_bucket(items)

        # Assert
        assert answer == 400
        assert data == 'BadRequest'

    # post_bucket not checking exist name(test fail 7)
    def test_post_bucket_with_many_items_with_exist_name(self):
        """
        Should return BadRequest (400)
        """

        # Arrange
        items = {100: {'name': 'test1',
                       'amount': 100, 'qty': 4},
                 200: {'name': 'test2',
                       'amount': 525, 'qty': 5}}
        # Act
        answer, data = FakeWebService.post_bucket(items)

        # Assert
        assert answer == 400
        assert str(data) == 'Already existed'


class Test_delete_item:
    def test_delete_item_with_exist_id(self):
        """
        Should return None (200)
        """

        # Arrange
        id_item = 1

        # Act
        answer, data = FakeWebService.delete_item(id_item)

        # Assert
        assert answer == 200
        assert data is None

    # delete_item not cheking delete id (test fail 8)
    def test_delete_item_with_not_exist_id(self):
        """
        Should return Not found (404)
        """

        # Arrange
        id_item = 10

        # Act
        answer, data = FakeWebService.delete_item(id_item)

        # Assert
        assert answer == 404
        assert data == 'Not found'


class Test_post_clear:
    def test_post_clear(self):
        """
        Should clear service (200)
        """

        # Act
        answer, data = FakeWebService.post_clear()

        # Assert
        assert answer == 200
        assert data is None

