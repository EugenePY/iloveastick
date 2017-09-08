# -*- coding= utf-8
from collections import OrderedDict, defaultdict


class MyOrderDict(OrderedDict):
    def __str__(self):
        return "OrderedDict{}".format(
            ",".join(["{}: {}".format(i, j) for i ,j in self.items()]))


class MySet(set):
    def __str__(self):
        return "set({})".format(",".join(["{}".format(i) for i in self]))


class Graph(object):
    """ Graph data structure, undirected by default. """

    def __init__(self, connections):
        self._graph = MyOrderDict()
        self.add_connections(connections)
        self.check_order()

    def add_connections(self, connections):
        """ Add connections (list of tuple pairs) to graph """
        for node1, node2 in connections:
            self.add(node1, node2)

    def add(self, node1, node2):
        """ Add connection between node1 and node2 """
        if self._graph.has_key(node1):
            self._graph[node1].add(node2)
        else:
            self._graph[node1] = MySet([node2])

    def _check_order(self, level_root, next_levevl_root):
        """ the node of next level should be the leaf of last level"""
        if not (next_levevl_root in self._graph[level_root]):
            raise "The graph is not valid the node {} is ordered conflict." + \
                    "{}".format(level_root.name, next_levevl_root.name)

    def check_order(self):
        temp = None
        for parent, child in self._graph.items()[::-1]:
            print parent, child

    def remove(self, node):
        """ Remove all references to node """

        for n, cxns in self._graph.iteritems():
            try:
                cxns.remove(node)
            except KeyError:
                pass
        try:
            del self._graph[node]
        except KeyError:
            pass

    def is_connected(self, node1, node2):
        """ Is node1 directly connected to node2 """
        return node1 in self._graph and node2 in self._graph[node1]

    def __str__(self):
        return '{}({})'.format(self.__class__.__name__, dict(self._graph))


class Node(object):
    """class Node define the e situation of current talk node.
    """

    def __init__(self, name, intent=None, event=None, action=None):
        self.name = name
        if intent is None:
            intent = "default"

        self.intent = intent
        self.action = action


    def __str__(self):
        return "({},name={}, intent={}, act={})".format(
            self.__class__.__name__, self.name, self.intent, self.action)

    def add_action(self):
        pass


class Root(Node):
    def __init__(self, *arg, **kwarg):
        super(Root, self).__init__(*arg, **kwarg)


class Action(object):
    """define the reply mode"""
    action_tag = None
    node = None

    def _apply(self, action):
        pass

    def apply(self, request):
        do = None
        r = self._apply(do)
        return r

class Query(Action):
    pass

class Reply(Action):
    pass

class QueryUserLoaction(Action):
    action_tag = "query.location"

    def __init__(self, name):
        self.name = name

    def action(self, respone):
        if respone['action'] == self.action_tag:
            data = {"facebook": {"text": respone[
                'fulfillment']['message'][0]['speech'],
                "quick_replies"=[{"content_type": "location"}]} }
            return data
        else:
            return {}


class PostRestaurantEvent(Action):
    action_tag = "post.restaurant_event"

    def __init__(self, name):
        self.name = name

    def action(self, respone):
        pass



class Agent(Graph):
    def __init__(self, *arg, **kwarg):
        super(Agent, self).__init__(*arg, **kwarg)

    @staticmethod
    def parse_node(cls, response):
        current_node = Node(name=respone['message']['text'],
             context=respone['context'],
             intent=respone['metadata']['intentName'])
        return current_node

    def action(self, response):
        return {}


if __name__ == "__main__":
    root = Root(name='打招呼')
    a = Node(name='打招呼', event="Greeting")
    b = Node(name='直接說我要找餐廳', intent="find")
    c = Node(name='開找', intent="find")
    d = Node(name='幹', intent="find")

    agent = Agent(connections=[(root, a), (root, b), (b, c), (a, c)])
    result = agent.action(response)

