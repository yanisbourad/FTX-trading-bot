# présentation
Ce trading Bot a été implémenté pour vous aider à saisir quelques opportunités du marché en suivant les tendances. Nous avons utilisé la méthode de l'alligator, qui consiste à comparer 6 EMA, avec les paramètres respectives 7, 30, 50, 100, 121, 200 ( vous pouvez les changer si vous pensez que vous pouvez avoir de meilleur résultat). Nous allons acheter lorsque EMA1 > EMA2 > EMA3> EMA4  > EMA5 > EMA6. De plus, nous allons nous assurer que nous ne sommes pas en sur-achat lorsqu'on regarde notre RSI. Pour la vente, nous allons nous assurer que notre EMA6 est supérieur à EMA1 et que nous ne sommes pas en sur-vente lorsqu'on consulte notre RSI.
Pour être communiqué des achats/vente, vous serez notifié via un channel discord que vous aurez crée

# Précaution
Ce bot a tendance de bien marcher lorsqu'on le fait marcher à chaque heure. Il peut être mis sur un serveur, comme google Cloud ou Amazon Server, ou peut être exécuter sur votre ordinateur (celui-ci doit être tout le temps allumé)

# Pré-requis
Vous devez installer discord, ta, pandas et ftx pour pouvoir les import correctement dans votre fichier python. De plus, vous devez vous créer un bot discord qui sera capable d'afficher les messages dans le channel

# BackTest
- Lorsque vous avez une stratégie, il faut la tester pour voir si elle en vaut la peine. Cette classe permet donc de tester vos stratégies selon une période de votre choix. Attention! les résultats du passé ne garantissent pas les résultat du futur.

# ftxBot
- Ce fichier contient tous les données du compte FTX à l'aide de l'API Key et l'API secret (quantité d'USDT, ou d'un coin), Attention! ces API sont des données confidentielles.
- lorsqu'une opportunité se présente, cette classe permet d'effectuer des achats/ ventes au prix du marché. De plus, a chaque heure, vous recevrez une notification discord, qui vous préviendra s'il a acheté, vendu, ou attendre une opportunité
