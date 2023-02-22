
class FakeWebService(object):

    Data = {1: {'name': 'test1',
                'amount': 100, 'qty': 4},
          2: {'name': 'test2',
                'amount': 525, 'qty': 5},
          3: {'name': 'test3',
                'amount': 10, 'qty': 1}
          }

    @staticmethod
    def get_items():
        return (200, FakeWebService.Data)

    @staticmethod
    def get_item(id_):
        if id_ in FakeWebService.Data:
            return (200, FakeWebService.Data[id_])
        else:
            return (404, 'Not found')

    @staticmethod
    def post_item(item):
        '''
        item: {'id': A, 'name': '', 'amount: X, 'qty': Y}
        '''
        id_ = item.pop('id')
        if id_ is None:
            return (400, 'BadRequest')

        name_ = item.get('name', None)
        if not name_:
            return (400, 'BadRequest')
        if name_ in [FakeWebService.Data[x]['name'] for x in FakeWebService.Data]:
            return (400, 'Already existed')

        amount_ = item.get('amount')
        if not amount_:
            return (400, 'BadRequest')

        FakeWebService.Data[id_] = item
        return (200, None)

    @staticmethod
    def delete_item(id_):
        FakeWebService.Data.pop(id_)
        return (200, None)

    @staticmethod
    def patch_decrease(id_):
        item_ = FakeWebService.Data[id_]
        amount_ = item_['amount']
        qty_ = item_['qty']
        price = amount_ / qty_

        FakeWebService.Data[id_]['qty'] = qty_ - 1
        FakeWebService.Data[id_]['amount'] = price * FakeWebService.Data[id_]['qty']

        return (200, FakeWebService.Data[id_])

    @staticmethod
    def patch_increase(id_):
        item_ = FakeWebService.Data[id_]
        amount_ = item_['amount']
        qty_ = item_['qty']
        price = amount_ / qty_

        FakeWebService.Data[id_]['qty'] = qty_ + 1
        FakeWebService.Data[id_]['amount'] = price * FakeWebService.Data[id_]['qty']

        return (200, FakeWebService.Data[id_])

    @staticmethod
    def post_bucket(bucket):
        '''
        bucket: {
                  N1: {'name': '', 'amount: X1, 'qty': Y1},
                  N2: {'name': '', 'amount: X2, 'qty': Y2},
              }
        '''
        FakeWebService.Data.update(bucket)

    @staticmethod
    def post_clear():
        for key in [x for x in FakeWebService.Data.keys()]:
            if key:
                FakeWebService.Data.pop(key)
        return (200, None)

