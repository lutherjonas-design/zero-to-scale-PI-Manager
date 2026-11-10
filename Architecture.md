# Command Registry / Outside Input
**Input Schema:**
{path:str, action:str, payload:[OPTIONAL]}
**Registry tagging in Interfaces:**
* system: everything that is directly on the PI, like the CLI or hooks from the bare Repos
* internal: communication between selector components, i.e. no direct interaction to the outside. An example would be a backup triggered in the health block, needing to tell the Service to prepare for the task and to pause it tasks
* public: everything that get's exposed trough api routes and is not part of forward-auth
* forward-auth: for everything traefik needs to interact with the manager, for example waking containers
Even if this seperates the design from typical Interfaces, since Python lacks this in general, a better overview for developers and the enabling of a better automatic discovery made me choose this
# Interface design
Atleast for the Interfaces that are meant for commands the following Pattern will be enforced by the autodiscovery Feature:
**above the class:**
@selector_namespace("SELECTOR") 
# Outer Layer