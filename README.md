Introduction
====

When a major disaster occurs, to reduce the numbers of deaths and injuries, much resource will be released and be used by citizens. For example, tourists can get local shelter information and head for them to protect themselves. Rescue workers can get building internal information to save victims. However, during an emergency and network is not working, people lose their head because they cannot get website information. Thus, they don’t know how process next action.

We design a software called Point of Service Server (POS), it can be deployed on various platform like desktop, laptop, smartphone, and embedded board etc. it usually can receive information sent by provider. Then, if there have an emergency and result network failed, people can find public machine which have installed POS to download, and many kind people can devote their machine which also have installed POS to solve that many panic people who not get information.

Functionality
====

Publish/Subscribe pattern (Pub/Sub pattern): POS plays a subscribe role. It can register to data provider platform and waits to receive topic they subscribe periodically.

Web socket: It is for smartphone which have a dynamic IP address. When POS’ floating IP is from A to B and disconnect with data provider, it will re-connect again to receive message.

Hook accountability: some private data need validation and authorization. POS will activate an accountability mechanism if user accesses data. 

Download: POS platform provides some interface for user to download. For example, smartphone provide Bluetooth, desktop and laptop provide USB and memory card. 

