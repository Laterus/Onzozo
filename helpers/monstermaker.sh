read -p 'Monster Name: ' monvar
read -p 'Description: ' descvar
read -p 'Health Pool: ' hpvar
read -p 'Power: ' powvar
read -p 'Defense: ' defvar
read -p 'Type: ' typevar

echo
echo $monvar:
echo "    "desc: "'$descvar'"
echo "    "type: $typevar
echo "    "base_stats:
echo "        "hp: $hpvar
echo "        "pow: $powvar
echo "        "def: $defvar
